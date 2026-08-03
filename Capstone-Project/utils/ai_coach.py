import os
from typing import Dict, Any, Optional


DEFAULT_GEMINI_MODELS = (
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
)

MIN_COACH_RESPONSE_WORDS = 40


def _get_response_text(response: Any) -> str:
    """Return Gemini response text without hiding blocked/empty responses."""
    try:
        text = getattr(response, "text", "")
    except ValueError:
        return ""

    return text.strip() if text else ""


def _looks_incomplete_response(text: str) -> bool:
    if len(text.split()) < MIN_COACH_RESPONSE_WORDS:
        return True

    return text[-1] not in ".!?"


def create_coaching_prompt(summary_data: Dict[str, Any]) -> str:
    """
    Create a detailed coaching prompt for Gemini based on user data.

    Args:
        summary_data: Dictionary containing day summary metrics

    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a sharp, no-nonsense productivity coach who gives brutally honest but actionable advice about screen time. Your tone is direct and slightly blunt, like a tough personal trainer, but ultimately supportive and constructive.

ANALYZE THIS DAY'S SCREEN TIME DATA:

KEY METRICS:
- Date: {summary_data.get('date', 'Unknown')}
- Total Screen Time: {summary_data.get('total_minutes', 0)} minutes
- Daily Goal: {summary_data.get('daily_goal', 180)} minutes
- Status: {'OVER goal' if summary_data.get('total_minutes', 0) > summary_data.get('daily_goal', 180) else 'UNDER goal'}

TOP APP:
- {summary_data.get('most_used_app', 'Unknown')}: {summary_data.get('most_used_minutes', 0)} minutes

CATEGORY BREAKDOWN:
"""
    
    for category_data in summary_data.get("category_breakdown", []):
        prompt += f"- {category_data['Category']}: {category_data['Minutes']} minutes\n"
    
    prompt += """
REQUIRED RESPONSE FORMAT:
Write exactly 4 short paragraphs. Do not use headings.
Keep the full response between 120 and 170 words.
Every paragraph must be complete. Do not stop mid-sentence.

Paragraph 1: Start with a blunt 1-2 sentence verdict about this day's screen habits.

Paragraph 2: Analyze the category distribution:
   - If social media/entertainment dominates (over 40%), call it out directly
   - If education/coding/productivity is strong, acknowledge it briefly
   - Identify the biggest time-wasting pattern

Paragraph 3: Give exactly 3 specific, actionable substitutions based on what they were doing:
   - If heavy social media: suggest walking, stretching, meal prep, reading a physical book, journaling, coding practice, cleaning workspace, calling a friend
   - If heavy entertainment: suggest learning a new skill, exercise, creative hobbies, networking
   - If heavy communication: suggest focused work blocks, deep work sessions
   - Make substitutions specific and realistic for the type of person who uses these apps

Paragraph 4: End with one concrete, measurable goal for tomorrow (e.g., "Tomorrow, keep social media under 45 minutes" or "Replace 30 minutes of TikTok with 30 minutes of coding practice").

TONE RULES:
- Be blunt but not abusive
- Use phrases like "Look, here's the reality..." or "Let's be honest..."
- Never just say "use your phone less"
- Provide specific, realistic alternatives
- End on an encouraging but firm note
- Keep it concise, but always finish the final sentence

Remember: You're a tough coach who wants them to succeed, not a gentle therapist."""
    
    return prompt


def get_coach_response(summary_data: Dict[str, Any], api_key: Optional[str] = None) -> Optional[str]:
    """
    Generate a personalized coaching response from the Gemini API.

    Args:
        summary_data: Dictionary containing day summary metrics
        api_key: Optional Gemini API key. If not provided, the key is read
            from the GEMINI_API_KEY environment variable.

    Returns:
        The coaching response string, or an error/fallback message.
    """
    # Get API key from parameter or environment
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "API key not configured. Please add GEMINI_API_KEY to your .env file."

    try:
        import google.generativeai as genai
    except ImportError:
        return (
            "Gemini support is not installed. Run "
            "`pip install -r requirements.txt` and restart the app."
        )

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Create prompt
        prompt = create_coaching_prompt(summary_data)
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
        }
        configured_model = os.getenv("GEMINI_MODEL")
        model_names = (
            (configured_model,) + DEFAULT_GEMINI_MODELS
            if configured_model
            else DEFAULT_GEMINI_MODELS
        )

        last_error = None
        for model_name in dict.fromkeys(model_names):
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=generation_config,
                )
                response = model.generate_content(prompt)
                response_text = _get_response_text(response)
                if response_text and not _looks_incomplete_response(response_text):
                    return response_text

                last_error = (
                    f"{model_name} returned an incomplete response: "
                    f"{response_text[:120] or 'no text'}"
                )
            except Exception as model_error:
                last_error = model_error
                error_text = str(model_error).lower()
                if "not found" not in error_text and "supported for generatecontent" not in error_text:
                    raise

        return (
            "Unable to generate a complete coaching response. Please try again. "
            f"Last Gemini result: {last_error}"
        )

    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper():
            return "Invalid API key. Please check your GEMINI_API_KEY in .env file."
        elif "quota" in error_msg.lower():
            return "API quota exceeded. Please try again later or check your billing settings."
        else:
            return f"Unable to generate coaching response: {error_msg}"
