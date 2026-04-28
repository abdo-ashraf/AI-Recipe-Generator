import streamlit as st
from langchain_components.chains import Orchestrator
from langchain_components.models import RecipeResult

st.set_page_config(page_title="AI Recipe Generator", layout="centered")
st.title("AI Recipe Generator — وصفة مع LLM")

with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("LLM Provider", options=["openai", "huggingface", "openrouter"], index=0)
    provider_label_map = {
        "openai": "OpenAI API key",
        "huggingface": "Hugging Face API key",
        "openrouter": "OpenRouter API key",
    }
    provider_label = provider_label_map.get(provider, "Provider API key")
    provider_api_key = st.text_input(provider_label, type="password")
    mode = st.selectbox("Mode", options=["strict", "natural", "creative"], index=1)
    language = st.selectbox("Output language", options=["Arabic", "English"], index=0)
    show_raw_output = st.checkbox("Show raw output", value=False)

ingredients = st.text_area("Enter your ingredients (one line or comma separated):", height=150)
# lang = st.radio("Language / اللغة:", options=["Arabic", "English"]) 


def render_recipe_result(result: RecipeResult, show_raw_output: bool) -> None:
    st.subheader("Parsed Output")
    parsed = result.parsed
    st.markdown(f"**Title:** {parsed.title}")

    estimated_time = parsed.estimated_time if parsed.estimated_time is not None else "N/A"
    estimated_calories = parsed.estimated_calories if parsed.estimated_calories is not None else "N/A"
    estimated_cost = parsed.estimated_cost if parsed.estimated_cost is not None else "N/A"

    st.markdown(
        f"**Estimated time:** {estimated_time} minutes | "
        f"**Estimated calories:** {estimated_calories} kcal | "
        f"**Estimated cost:** {estimated_cost}"
    )

    if parsed.ingredients:
        st.markdown("**Ingredients:**")
        for item in parsed.ingredients:
            st.write(f"- {item}")

    if parsed.steps:
        st.markdown("**Steps:**")
        for step in parsed.steps:
            st.write(f"- {step}")

    if parsed.alternatives:
        st.markdown("**Alternatives:**")
        for alternative in parsed.alternatives:
            st.write(f"- {alternative}")

    if show_raw_output:
        st.subheader("Raw Output")
        st.code(result.raw)

if st.button("Generate Recipe"):
    if not ingredients.strip():
        st.error("Please provide ingredients.")
    else:
        with st.spinner("Generating..."):
            try:
                orchestrator = Orchestrator(
                    provider_name=provider,
                    api_key=provider_api_key or None,
                )
                result = orchestrator.generate_recipe(ingredients, language=language, mode=mode)
                render_recipe_result(result, show_raw_output)
            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Error: {e}")
