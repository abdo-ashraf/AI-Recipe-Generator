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
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

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
                    temperature=temperature,
                    api_key=provider_api_key or None,
                )
                result = orchestrator.generate_recipe(ingredients)
                st.subheader("Raw Output")
                st.code(result.get("raw", ""))
                st.subheader("Parsed Output")
                parsed = result.get("parsed", {})
                st.markdown(f"**Title:** {parsed.get('title')}")
                st.markdown(f"**Time:** {parsed.get('time')} | **Calories:** {parsed.get('calories')} | **Cost:** {parsed.get('cost')}")
                st.markdown("**Ingredients:**")
                for it in parsed.get("ingredients", []):
                    st.write(f"- {it}")
                st.markdown("**Steps:**")
                for s in parsed.get("steps", []):
                    st.write(f"- {s}")
            except ValueError as e:
                st.error(f"Configuration error: {e}")
            except Exception as e:
                st.error(f"Error: {e}")
