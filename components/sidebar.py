import streamlit as st

from config.settings import AzureConfigStatus


def render_sidebar(config_status: AzureConfigStatus) -> None:
    with st.sidebar:
        st.header("System Status")
        st.write("Local recipe CSV: ready")

        if config_status.vision_ready:
            st.success("Azure AI Vision: configured")
        else:
            st.warning("Azure AI Vision: missing .env values")

        if config_status.speech_ready:
            st.success("Azure Speech to Text: configured")
        else:
            st.warning("Azure Speech to Text: missing .env values")

        st.divider()
        st.markdown("**Inputs used for scoring**")
        st.write("Text preference")
        st.write("Image caption, tags, objects, OCR")
        st.write("Voice transcript")
