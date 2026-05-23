import streamlit as st


def render_combined_text(combined_text: str, active_sources=None) -> None:
    with st.expander("Combined search profile", expanded=False):
        if active_sources:
            st.write(f"**Input source used:** {', '.join(active_sources)}")
        if combined_text:
            st.write(combined_text)
        else:
            st.write(
                "No usable text has been extracted yet. You can use text only, image only, "
                "speech only, or combine multiple input types."
            )


def render_recommendations(
    recommendations,
    uploaded_image=None,
    image_analysis=None,
    active_sources=None,
) -> None:
    st.subheader("Ranked Meal Recommendations")

    if active_sources:
        st.caption(f"Recommendation based on: {', '.join(active_sources)}")
    else:
        st.info(
            "Add at least one input source: text, image, speech, or any combination of them."
        )

    if uploaded_image:
        with st.container(border=True):
            st.markdown("### Uploaded image used for recommendation")
            st.image(uploaded_image, use_container_width=True)
            if image_analysis:
                caption = image_analysis.get("caption")
                keywords = image_analysis.get("keywords", [])
                if caption:
                    st.write(f"**Azure caption:** {caption}")
                if keywords:
                    st.write(f"**Azure keywords:** {', '.join(keywords)}")

    if recommendations.empty:
        st.warning(
            "No strong recipe matches yet. Try adding a clear ingredient, cuisine, "
            "diet keyword, or make sure Azure Vision/Speech credentials are configured."
        )
        return

    for rank, (_, recipe) in enumerate(recommendations.iterrows(), start=1):
        with st.container(border=True):
            top_line = f"{rank}. {recipe['name']} - score {recipe['score']}"
            st.markdown(f"### {top_line}")
            meta = (
                f"**Cuisine:** {recipe['cuisine']}  |  "
                f"**Meal:** {recipe['meal_type']}  |  "
                f"**Time:** {recipe['prep_time']} min"
            )
            st.markdown(meta)
            if "main_protein" in recipe and recipe["main_protein"]:
                st.write(f"**Main protein match:** {recipe['main_protein']}")
            st.write(f"**Ingredients:** {recipe['ingredients']}")
            st.write(f"**Tags:** {recipe['tags']}")
            st.write(f"**Why recommended:** matched {recipe['matched_terms']}")
