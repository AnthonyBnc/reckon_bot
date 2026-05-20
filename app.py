import streamlit as st

from components.input_section import (
    render_image_input,
    render_text_input,
    render_voice_input,
)
from components.results import render_combined_text, render_recommendations
from components.sidebar import render_sidebar
from config.settings import get_config_status
from services.azure_speech import transcribe_audio
from services.azure_vision import analyse_image
from services.data_loader import load_recipes
from services.recommender import recommend_recipes


def main() -> None:
    st.set_page_config(
        page_title="Smart Meal Recommendation Bot",
        layout="wide",
    )

    config_status = get_config_status()
    render_sidebar(config_status)

    st.title("Smart Meal Recommendation Bot")
    st.caption(
        "Option 2 build: text preferences, ingredient image analysis, voice input, "
        "Azure AI services, local CSV recipes, and explainable recommendations."
    )

    recipes = load_recipes()

    left_col, right_col = st.columns([1, 1], gap="large")
    with left_col:
        typed_text = render_text_input()
        uploaded_image = render_image_input()
        recorded_audio = render_voice_input()

    image_analysis = {}
    voice_text = ""

    with right_col:
        st.subheader("AI Extraction")

        if uploaded_image:
            with st.spinner("Analysing image with Azure AI Vision..."):
                image_analysis = analyse_image(uploaded_image.getvalue())
            if image_analysis.get("error"):
                st.warning(image_analysis["error"])
            st.write("**Image caption**")
            st.info(image_analysis.get("caption") or "No caption detected.")
            st.write("**Visual keywords**")
            st.write(", ".join(image_analysis.get("keywords", [])) or "No visual keywords found.")
            if image_analysis.get("ocr_text"):
                st.write("**OCR text**")
                st.write(image_analysis["ocr_text"])

        if recorded_audio:
            with st.spinner("Transcribing voice preference with Azure Speech to Text..."):
                voice_text = transcribe_audio(recorded_audio.getvalue())
            st.write("**Voice transcript**")
            st.success(voice_text or "No speech transcript returned.")

        if not uploaded_image and not recorded_audio:
            st.info("Upload an image or record a voice preference to see Azure extraction output.")

    combined_parts = [
        typed_text,
        image_analysis.get("caption", ""),
        " ".join(image_analysis.get("keywords", [])),
        image_analysis.get("ocr_text", ""),
        voice_text,
    ]
    combined_text = " ".join(part for part in combined_parts if part).strip()

    render_combined_text(combined_text)

    if st.button("Recommend Meals", type="primary", use_container_width=True):
        recommendations = recommend_recipes(recipes, combined_text)
        render_recommendations(recommendations)


if __name__ == "__main__":
    main()
