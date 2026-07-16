import os
import random
import requests
import streamlit as st
from PIL import Image
import io
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.responses.create(
    input="Explain the importance of fast language models",
    model="openai/gpt-oss-20b",
)
print(response.output_text)

st.title("AI Image Studio")
st.markdown("Generate stunning AI images with custom settings!")

with st.sidebar:
    st.title("-- Configurations --")
    st.divider()
    art_style = st.selectbox(
        "Art-Style",
        ["Realistic", "Anime", "CyberPunk", "Fantasy", "Watercolor"]
    )
    st.space()

    width = st.slider("Width", min_value=256, max_value=1024, value=512, step=64)
    height = st.slider("Height", min_value=256, max_value=1024, value=512, step=64)
    
    magic_enhance = st.checkbox("Enable Magic Enhance")
    st.divider()
    st.caption("Made with 💖 using Pollinations.ai")

col1, col2 = st.columns([2, 1])

with col1:
    user_prompt = st.text_area(
        "Enter your image description:",
        placeholder="eg. Beautiful sunset over mountains",
        height=100,
    )
    
    surprise_me = st.button("Surprise Me!!", use_container_width=True)
    
    generate = st.button("Generate Image", type="primary", use_container_width=True)
    
    if 'current_image' in st.session_state:
        img = st.session_state['current_image']
        prompt = st.session_state['current_prompt']
        
        clean_style = art_style.lower().replace(" ", "_")
        file_name = f"{clean_style}_image.png"
        
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_bytes = img_buffer.getvalue()
        
        st.download_button(
            label="Download Image",
            data=img_bytes,
            file_name=file_name,
            mime="image/png",
            type='secondary',
            use_container_width=True,
        )
    else:
        st.download_button(
            label="Download Image (Generate an image first)",
            data=b"",
            file_name="image.png",
            mime="image/png",
            type='secondary',
            use_container_width=True,
            disabled=True
        )
    
    if 'current_image' in st.session_state:
        with st.expander("Image Info"):
            st.write(f"**Prompt:** {st.session_state['current_prompt']}")
            st.write(f"**Style:** {art_style}")
            st.write(f"**Dimensions:** {width} x {height}")
            st.write(f"**Magic Enhance:** {'Active' if magic_enhance else 'Inactive'}")
            st.write(f"**File name:** {clean_style}_image.png")

with col2:
    st.subheader("PREVIEW")
    image_placeholder = st.empty()

def generate_image(prompt, width, height):
    full_prompt = f"{prompt}, {art_style} style"

    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on art station, unreal engine 5 render"
    
    url = f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            st.error(f"Error generating image: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None
    
if surprise_me:
    surprise_prompts = [
        "An astronaut riding a horse on Mars with a neon sunset",
        "A cyberpunk street food vendor in Tokyo with holographic signs",
        "A dragon made of galaxies flying through a nebula",
        "A steampunk city floating in the clouds with airships",
        "An underwater civilization with bio-luminescent buildings"
    ]

    random_prompt = random.choice(surprise_prompts)
    user_prompt = random_prompt
    st.success(f"Surprise Prompt: '{random_prompt}'")

    with st.spinner("Generating your surprise image..."):
        img = generate_image(random_prompt, width, height)
        if img:
            image_placeholder.image(img, caption=random_prompt, use_container_width=True)
            st.session_state['current_image'] = img
            st.session_state['current_prompt'] = random_prompt

if generate and user_prompt:
    with st.spinner("Creating your masterpiece..."):
        img = generate_image(user_prompt, width, height)
        if img:
            image_placeholder.image(img, caption=user_prompt, use_container_width=True)
            st.session_state['current_image'] = img
            st.session_state['current_prompt'] = user_prompt

st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with 💖 using Streamlit & Pollinations.ai</p>
        <p style='font-size: 12px;'>MirAI School of Technology - AI Builder Track 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)