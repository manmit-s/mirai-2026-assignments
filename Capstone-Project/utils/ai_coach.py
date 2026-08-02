"""
AI Coach module for Gemini API integration.
Provides personalized screen-time coaching based on user data.
"""

import os
from typing import Dict, Any, Optional


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

📊 Key Metrics:
- Date: {summary_data.get('date', 'Unknown')}
- Total Screen Time: {summary_data.get('total_minutes', 0)} minutes
- Daily Goal: {summary_data.get('daily_goal', 180)} minutes
- Status: {'OVER goal' if summary_data.get('total_minutes', 0) > summary_data.get('daily_goal', 180) else 'UNDER goal'}

📱 Top App:
- {summary_data.get('most_used_app', 'Unknown')}: {summary_data.get('most_used_minutes', 0)} minutes

📂 Category Breakdown:
"""
    
    for category_data in summary_data.get('category_breakdown', []):
        prompt += f"- {category_data['Category']}: {category_data['Minutes']} minutes\n"
    
    prompt += """
REQUIRED RESPONSE FORMAT:
1. START with a 1-2 sentence blunt verdict about this day's screen habits.

2. ANALYZE the category distribution:
   - If social media/entertainment dominates (over 40%), call it out directly
   - If education/coding/productivity is strong, acknowledge it briefly
   - Identify the biggest time-wasting pattern

3. GIVE 3 SPECIFIC, ACTIONABLE SUBSTITUTIONS based on what they were doing:
   - If heavy social media: suggest walking, stretching, meal prep, reading a physical book, journaling, coding practice, cleaning workspace, calling a friend
   - If heavy entertainment: suggest learning a new skill, exercise, creative hobbies, networking
   - If heavy communication: suggest focused work blocks, deep work sessions   - Make substitutions specific and realistic for the type of person who uses these apps

4. END with one concrete, measurable goal for tomorrow (e.g., "Tomorrow, keep social media under 45 minutes" or "Replace 30 minutes of TikTok with 30 minutes of coding practice")

TONE RULES:
- Be blunt but not abusive
- Use phrases like "Look, here's the reality..." or "Let's be honest..."
- Never just say "use your phone less"
- Provide specific, realistic alternatives
- End on an encouraging but firm note
- Keep total response under 250 words

Remember: You're a tough coach who wants them to succeed, not a gentle therapist."""
    
    return prompt


def get_coach_response(summary_data: Dict[str, Any], api_key: Optional[str] = None) -> Optional[str]:

    try:
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
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 500,
            }
        )
        
        # Create prompt
        prompt = create_coaching_prompt(summary_data)
        
        # Generate response
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper():
            return "Invalid API key. Please check your GEMINI_API_KEY in .env file."
        elif "quota" in error_msg.lower():
            return "API quota exceeded. Please try again later or check your billing settings."
        else:
            return f"Unable to generate coaching response: {error_msg}"
