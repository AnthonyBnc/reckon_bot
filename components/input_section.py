import streamlit as st


def render_text_input() -> str:
    st.subheader("1. Text Preference")
    return st.text_area(
        "What kind of meal do you want?",
        placeholder="Example: quick healthy high protein dinner with chicken and rice",
        height=120,
    )


def render_image_input():
    st.subheader("2. Ingredient or Food Image")
    return st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        help="Azure AI Vision extracts captions, tags, objects, and OCR text.",
    )


def render_voice_input():
    st.subheader("3. Voice Preference")
    if hasattr(st, "audio_input"):
        return st.audio_input("Record a short preference")

    return st.file_uploader(
        "Upload a short audio file",
        type=["wav"],
        help="Your Streamlit version does not expose audio recording, so WAV upload is used.",
    )
