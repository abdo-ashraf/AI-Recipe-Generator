import streamlit as st
from langchain_components.chains import Orchestrator

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
                st.subheader("Parsed Output")
                parsed = result.get("parsed", {})
                st.markdown(f"**Title:** {parsed.get('title', 'N/A')}")
                st.markdown(f"**Language:** {parsed.get('language', language)}")
                st.markdown(
                    f"**Estimated time:** {parsed.get('estimated_time', 'N/A')} minutes | "
                    f"**Estimated calories:** {parsed.get('estimated_calories', 'N/A')} kcal | "
                    f"**Estimated cost:** {parsed.get('estimated_cost', 'N/A')}"
                )

                ingredients_list = parsed.get("ingredients", [])
                if ingredients_list:
                    st.markdown("**Ingredients:**")
                    for item in ingredients_list:
                        st.write(f"- {item}")

                steps_list = parsed.get("steps", [])
                if steps_list:
                    st.markdown("**Steps:**")
                    for step in steps_list:
                        st.write(f"- {step}")

                alternatives_list = parsed.get("alternatives", [])
                if alternatives_list:
                    st.markdown("**Alternatives:**")
                    for alternative in alternatives_list:
                        st.write(f"- {alternative}")

                if show_raw_output:
                    st.subheader("Raw Output")
                    st.code(result.get("raw", ""))
            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Error: {e}")
