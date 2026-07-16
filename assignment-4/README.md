# AI Image Studio

An AI-powered image generation app built with Streamlit and Pollinations.ai.

## Features

- **Custom Dimensions** — Width and height sliders (256–1024px) control output size
- **Art Styles** — Choose from Realistic, Anime, CyberPunk, Fantasy, or Watercolor
- **Magic Enhance** — Toggle to add quality boost words for better AI results
- **Surprise Me** — Random creative prompts for instant inspiration
- **Download** — Save generated images with dynamic filenames

## Setup

```bash
pip install streamlit requests pillow
streamlit run app.py
```

## Tasks Completed

1. **URL Parameters** — Width/height sliders now passed to Pollinations API
2. **File Extension** — Downloads use `.png` extension with dynamic naming
3. **Magic Enhance** — Checkbox appends enhancement keywords to prompts
4. **Surprise Me** — Random prompt generator with one-click image creation

## Tech Stack

- Python, Streamlit, Pollinations.ai, Pillow