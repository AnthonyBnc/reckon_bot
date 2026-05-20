import streamlit as st


def render_combined_text(combined_text: str) -> None:
    with st.expander("Combined search profile", expanded=False):
        if combined_text:
            st.write(combined_text)
        else:
            st.write("No input has been provided yet.")


def render_recommendations(recommendations) -> None:
    st.subheader("Ranked Meal Recommendations")

    if recommendations.empty:
        st.warning("No strong recipe matches yet. Try adding ingredients, cuisine, or diet keywords.")
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
            st.write(f"**Ingredients:** {recipe['ingredients']}")
            st.write(f"**Tags:** {recipe['tags']}")
            st.write(f"**Why recommended:** matched {recipe['matched_terms']}")
