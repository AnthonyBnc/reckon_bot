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
from services.ingredient_detector import enrich_image_analysis_with_ingredients
from services.recommender import recommend_recipes


def build_input_profile(typed_text: str, image_analysis: dict, voice_text: str) -> tuple[str, list[str]]:
    profile_parts = []
    active_sources = []

    typed_text = typed_text.strip()
    if typed_text:
        profile_parts.append(typed_text)
        active_sources.append("Text")

    image_ingredients = image_analysis.get("ingredients", [])
    if image_ingredients:
        image_parts = [
            " ".join(image_ingredients),
            image_analysis.get("ocr_text", ""),
        ]
    else:
        image_parts = [
            image_analysis.get("ocr_text", ""),
        ]
    image_text = " ".join(part for part in image_parts if part).strip()
    if image_text:
        profile_parts.append(image_text)
        active_sources.append("Image")

    voice_text = voice_text.strip()
    if voice_text:
        profile_parts.append(voice_text)
        active_sources.append("Speech")

    return " ".join(profile_parts).strip(), active_sources


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
                image_analysis = enrich_image_analysis_with_ingredients(image_analysis, recipes)
            if image_analysis.get("error"):
                st.warning(image_analysis["error"])
            st.write("**Specific ingredients detected**")
            st.success(
                ", ".join(image_analysis.get("ingredients", []))
                or "No specific recipe ingredient detected from the image."
            )
            with st.expander("Raw Azure Vision output"):
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

    combined_text, active_sources = build_input_profile(
        typed_text=typed_text,
        image_analysis=image_analysis,
        voice_text=voice_text,
    )

    render_combined_text(combined_text, active_sources)

    if st.button("Recommend Meals", type="primary", use_container_width=True):
        recommendations = recommend_recipes(recipes, combined_text)
        render_recommendations(
            recommendations,
            uploaded_image=uploaded_image,
            image_analysis=image_analysis,
            active_sources=active_sources,
        )


if __name__ == "__main__":
    main()
