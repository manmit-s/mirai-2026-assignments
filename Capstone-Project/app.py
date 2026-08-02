from pathlib import Path
import os
import urllib.parse

import streamlit as st
from dotenv import load_dotenv

from utils.data_loader import load_data, filter_by_date, get_trend_data, get_category_summary
from utils.helpers import format_minutes, severity_classification, goal_comparison_text
from utils.ai_coach import get_coach_response


APP_DIR = Path(__file__).parent


st.set_page_config(
    page_title="Life-OS | Wellbeing Dashboard",
    page_icon=":material/self_improvement:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
    .main {
        background-color: #f8f9fa;
    }

    .app-header {
        background: linear-gradient(135deg, #445f9d 0%, #6f3f82 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(68, 95, 157, 0.25);
    }

    .app-header h1 {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 0;
    }

    .app-header p {
        font-size: 1.05rem;
        opacity: 0.95;
        font-weight: 300;
        margin: 0;
    }

    .section-header {
        font-size: 1.45rem;
        font-weight: 600;
        color: #243447;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #445f9d;
        display: inline-block;
        letter-spacing: 0;
    }

    .coaching-panel {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        margin: 1rem 0 2rem 0;
    }

    .accountability-box {
        background: linear-gradient(135deg, #2f7d7e 0%, #9b4d64 100%);
        padding: 1.5rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }

    .accountability-box code {
        white-space: pre-wrap;
        word-break: break-word;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main() -> None:
    """Run the Streamlit dashboard."""
    df = load_data(str(APP_DIR / "screentime.csv"))

    if df is None or df.empty:
        st.error("Failed to load screen-time data. Please check screentime.csv.")
        return

    st.markdown(
        """
        <div class="app-header">
            <h1>Life-OS Wellbeing Dashboard</h1>
            <p>Your screen-time coach for a more intentional digital life.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Controls")

        dates = sorted(df["Date"].unique())
        selected_date = st.selectbox(
            "Select date",
            dates,
            index=len(dates) - 1,
            help="Choose a date to analyze your screen-time habits.",
        )

        daily_goal = st.slider(
            "Daily screen-time goal (minutes)",
            min_value=30,
            max_value=480,
            value=180,
            step=15,
            help="Set your target daily screen-time limit.",
        )

        st.markdown("---")

        categories = sorted(df["Category"].dropna().unique())
        selected_categories = st.multiselect(
            "Filter categories",
            categories,
            default=categories,
            help="Select categories to include in analysis.",
        )

        st.markdown("---")

        show_all_data = st.toggle(
            "Show all data in charts",
            value=True,
            help="Show all available dates, or only the selected day.",
        )

        st.markdown("---")
        st.markdown("### Tip")
        st.info("Select different dates to see how your habits change over time.")

    if selected_categories:
        filtered_df = df[df["Category"].isin(selected_categories)]
    else:
        filtered_df = df.iloc[0:0]

    daily_data = filter_by_date(filtered_df, selected_date)

    st.markdown('<h2 class="section-header">Today\'s Snapshot</h2>', unsafe_allow_html=True)

    if daily_data.empty:
        st.warning(f"No data available for {selected_date}. Change the date or category filters.")
        return

    total_minutes = int(daily_data["Minutes_Used"].sum())
    app_totals = daily_data.groupby("App_Name")["Minutes_Used"].sum()
    category_totals = daily_data.groupby("Category")["Minutes_Used"].sum()
    most_used_app = app_totals.idxmax()
    most_used_minutes = int(app_totals.max())
    top_category = category_totals.idxmax()
    top_category_minutes = int(category_totals.max())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total screen time",
            value=format_minutes(total_minutes),
            delta=goal_comparison_text(total_minutes, daily_goal),
            delta_color="inverse",
        )

    with col2:
        st.metric(label="Most used app", value=most_used_app, delta=format_minutes(most_used_minutes))

    with col3:
        st.metric(label="Top category", value=top_category, delta=format_minutes(top_category_minutes))

    with col4:
        comparison = total_minutes - daily_goal
        st.metric(
            label="vs daily goal",
            value="Over goal" if comparison > 0 else "Under goal",
            delta=f"{abs(comparison)} min",
            delta_color="inverse" if comparison > 0 else "normal",
        )

    chart_df = filtered_df if show_all_data else daily_data
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<h2 class="section-header">Usage Trend</h2>', unsafe_allow_html=True)
        trend_data = get_trend_data(chart_df)
        if not trend_data.empty:
            st.line_chart(
                trend_data.set_index("Date")["Total_Minutes"],
                use_container_width=True,
                height=400,
            )

        goal_percentage = (total_minutes / daily_goal) * 100
        if goal_percentage > 150:
            st.warning(f"You are at {goal_percentage:.0f}% of your daily goal. Time to recalibrate.")
        elif goal_percentage > 100:
            st.info(f"You are at {goal_percentage:.0f}% of your daily goal. Slightly over, but manageable.")
        else:
            st.success(f"You are at {goal_percentage:.0f}% of your daily goal. Good work.")

    with col_right:
        st.markdown('<h2 class="section-header">Category Breakdown</h2>', unsafe_allow_html=True)
        category_summary = get_category_summary(chart_df, None if show_all_data else selected_date)
        if not category_summary.empty:
            st.bar_chart(
                category_summary.set_index("Category")["Minutes"],
                use_container_width=True,
                height=400,
            )

    st.markdown('<h2 class="section-header">App-Level Breakdown</h2>', unsafe_allow_html=True)
    app_breakdown = (
        daily_data.groupby(["Category", "App_Name"])["Minutes_Used"]
        .sum()
        .reset_index()
        .sort_values("Minutes_Used", ascending=False)
    )
    st.dataframe(
        app_breakdown,
        use_container_width=True,
        height=300,
    )

    st.markdown('<h2 class="section-header">AI Coach Analysis</h2>', unsafe_allow_html=True)
    st.markdown('<div class="coaching-panel">', unsafe_allow_html=True)

    load_dotenv(APP_DIR / ".env")
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.warning(
            "Gemini API key required for personalized coaching. Add "
            "`GEMINI_API_KEY=your_key_here` to `.env` and restart the app. "
            "Analytics still work without it."
        )
    else:
        with st.spinner("Your AI coach is analyzing your screen-time patterns..."):
            summary_data = {
                "date": selected_date,
                "total_minutes": total_minutes,
                "daily_goal": daily_goal,
                "most_used_app": most_used_app,
                "most_used_minutes": most_used_minutes,
                "top_category": top_category,
                "category_breakdown": get_category_summary(daily_data).to_dict("records"),
                "over_goal": total_minutes > daily_goal,
                "severity": severity_classification(total_minutes, daily_goal),
            }
            coaching_response = get_coach_response(summary_data, api_key)

        severity = severity_classification(total_minutes, daily_goal)
        if severity == "low":
            st.success("Great job keeping your screen time in check.")
        elif severity == "moderate":
            st.info("You are doing okay, but there is room to improve.")
        else:
            st.warning("High screen time detected. This is worth addressing.")

        st.markdown(coaching_response or "Failed to generate coaching response. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<h2 class="section-header">Accountability Partner</h2>', unsafe_allow_html=True)
    share_data = {
        "date": selected_date,
        "total_minutes": str(total_minutes),
        "goal": str(daily_goal),
        "status": "over" if total_minutes > daily_goal else "under",
    }
    query_string = urllib.parse.urlencode(share_data)
    base_url = st.query_params.get("base_url", "http://localhost:8501")
    shareable_url = f"{base_url}/?{query_string}"

    st.markdown('<div class="accountability-box">', unsafe_allow_html=True)
    st.markdown("### Share Your Progress")
    st.markdown(f"**Date:** {selected_date} | **Screen Time:** {format_minutes(total_minutes)}")
    st.markdown(f"**Status:** {'Over goal' if total_minutes > daily_goal else 'Under goal'}")

    col_share1, col_share2 = st.columns([3, 1])
    with col_share1:
        st.code(shareable_url, language=None)
    with col_share2:
        if st.button("Copy Link", use_container_width=True):
            st.success("Link ready to share.")

    st.markdown("Share this link with a friend to keep each other accountable.")
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
