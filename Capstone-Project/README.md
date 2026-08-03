# Life-OS Wellbeing Dashboard

A production-quality Streamlit dashboard for screen-time analysis with AI-powered coaching from Google's Gemini API. Built as a virtual internship project demonstrating SaaS-grade development practices.

## Features

- **Interactive Dashboard**: Clean, modern UI with real-time filtering and analytics
- **Screen-Time Analytics**: Track usage patterns across 14+ days with detailed breakdowns
- **AI Coaching**: Personalized, brutally honest coaching from Gemini based on your habits
- **Category Breakdown**: Visual analysis of time spent across different app categories
- **KPI Metrics**: Key performance indicators with goal tracking and delta comparisons
- **Shareable Accountability**: Generate shareable links to keep yourself accountable
- **Responsive Design**: Professional styling that feels like a real SaaS product

## Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas for analytics and data manipulation
- **AI Integration**: Google Gemini API (google-genai)
- **Visualization**: Streamlit native charts + Plotly
- **Environment**: Python-dotenv for secure API key management

## Project Structure

```
life-os-wellbeing-dashboard/
|-- app.py                  # Main Streamlit application
|-- screentime.csv          # Synthetic dataset (14+ days)
|-- requirements.txt        # Python dependencies
|-- .env                    # Environment variables (not tracked)
|-- .env.example            # Example environment configuration
|-- .gitignore              # Git ignore rules
|-- README.md               # Project documentation
|-- assets/
|   |-- logo.png            # App logo placeholder
|-- utils/
    |-- __init__.py         # Package initializer
    |-- data_loader.py      # Data loading and processing
    |-- ai_coach.py         # Gemini API integration
    |-- helpers.py          # Utility functions
```

## Quick Start

### Prerequisites

- Python 3.8+
- Git
- Google Gemini API key

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd life-os-wellbeing-dashboard
```

2. **Create and activate a virtual environment (recommended)**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Copy the example environment file and add your Gemini API key:

```bash
cp .env.example .env
```

Then edit `.env` and set:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

You can obtain a free API key from [Google AI Studio](https://aistudio.google.com/).

5. **Run the application**

```bash
streamlit run app.py
```

Your browser should open automatically at `http://localhost:8501`.

## Usage

1. **Select a date** from the sidebar to analyze a specific day's habits.
2. **Adjust your daily goal** slider to set a target screen-time limit.
3. **Filter categories** to focus on specific app types.
4. **Toggle charts** between all data and the selected day.
5. **Review the AI Coach Analysis** for personalized, actionable recommendations.
6. **Generate a shareable link** to keep yourself accountable with a friend.

## Features in Detail

### Today's Snapshot

Four KPI cards summarize the selected day:

- Total screen time versus your daily goal
- Most used app and its usage
- Top category and its usage
- Status versus goal (over or under)

### Usage Trend

A line chart shows total screen time across the available dates so you can spot weekly patterns and trends.

### Category Breakdown

A bar chart breaks down time spent across app categories (Social Media, Entertainment, Coding, Education, Productivity, and more).

### App-Level Breakdown

A sortable table shows every app grouped by category, with per-app minute totals.

### AI Coach Analysis

Powered by the Gemini API, this section delivers a blunt, personalized coaching message based on your actual usage data. The prompt asks for:

- A direct verdict on the day's habits
- Analysis of the category distribution
- Three specific, actionable substitutions
- One concrete, measurable goal for tomorrow

### Accountability Partner

Generates a shareable URL encoding the date, total screen time, goal, and status so you can share your progress with someone who can help keep you on track.

## Project Modules

### `app.py`

Main Streamlit entry point. Handles all UI rendering, user controls, data summaries, and the AI coach integration.

### `utils/data_loader.py`

Handles CSV parsing, date normalization, and all data aggregation helpers used to drive the dashboard's metrics and charts.

### `utils/ai_coach.py`

Encapsulates the Gemini API integration, including prompt construction and response generation with graceful fallbacks for missing or invalid API keys.

### `utils/helpers.py`

Provides small utility functions for formatting minutes, classifying severity, comparing against goals, and categorizing usage patterns.

## Troubleshooting

### The dashboard shows "Failed to load screen-time data"

- Make sure `screentime.csv` is in the project root.
- Verify the CSV contains the required columns: `Date`, `App_Name`, `Category`, `Minutes_Used`.

### AI Coach is not responding

- Confirm `GEMINI_API_KEY` is set in your `.env` file.
- Ensure you have installed the dependencies: `pip install -r requirements.txt`.
- Check your Gemini API quota and billing settings.

### Streamlit warns about runtime errors

- Run `pip install --upgrade streamlit` to ensure you have a recent version.
- Use a clean virtual environment to avoid dependency conflicts.

## Pre-Submission Checklist

### Functionality

- [x] Dashboard loads and displays screen-time data
- [x] Date selection, goal slider, and category filters work
- [x] KPI metrics update based on the selected day
- [x] Trend and category charts render correctly
- [x] App-level breakdown table is populated
- [x] AI Coach gracefully handles a missing API key
- [x] Accountability share link is generated correctly

### Code Quality

- [x] Clean and modular structure
- [x] Proper error handling
- [x] Meaningful function names and docstrings
- [x] No deprecated or unused code
- [x] Good separation of concerns

### Documentation

- [x] README is clear and up to date
- [x] Setup steps are easy to follow
- [x] Features are documented
- [x] No emoji or special symbol characters in source or docs

## Acknowledgements

**Built with:** Streamlit, Pandas, and Google Gemini API
**Course:** MirAI School of Technology - AI Builder Track 2026

