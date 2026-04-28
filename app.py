import streamlit as st
from langchain_components.chains import Orchestrator
from langchain_components.models import RecipeResult

st.set_page_config(
    page_title="AI Recipe Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# 🎨 Styles (FIXED + SCOPED)
# -----------------------------
def apply_custom_styles(is_rtl: bool = False):
    direction = "rtl" if is_rtl else "ltr"
    align = "right" if is_rtl else "left"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@500;700&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap');

    .block-container {{
        max-width: 900px;
        margin: auto;
    }}

    .app-container {{
        direction: {direction};
        text-align: {align};
        font-family: {'Noto Naskh Arabic, Tahoma' if is_rtl else 'Segoe UI'};
        /* Automatically switches between black and white text */
        color: var(--text-color); 
    }}

    textarea {{
        direction: {direction} !important;
        text-align: {align} !important;
        color: var(--text-color) !important;
        background-color: var(--background-color) !important;
        border: 1px solid var(--secondary-background-color) !important;
    }}

    .recipe-title {{
        font-size: 2.3em;
        font-weight: bold;
        color: #FF6B6B; /* Accent color stays the same for brand identity */
        text-align: center;
        margin-bottom: 20px;
    }}

    .stats-container {{
        display: flex;
        gap: 10px;
        margin: 20px 0;
    }}

    .stat-box {{
        flex: 1;
        /* Gradients look great in both modes */
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important; 
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }}

    .section-header {{
        font-size: 1.3em;
        font-weight: bold;
        color: #FF6B6B;
        margin: 20px 0 10px;
        border-bottom: 2px solid #4ECDC4;
        padding-bottom: 5px;
    }}

    .item {{
        /* Switches to light gray in Light Mode, dark gray in Dark Mode */
        background: var(--secondary-background-color); 
        color: var(--text-color);
        padding: 12px;
        border-radius: 6px;
        margin: 8px 0;
        border-{ "right" if is_rtl else "left" }: 4px solid #4ECDC4;
        transition: 0.2s;
    }}

    .item:hover {{
        transform: translateY(-2px);
        filter: brightness(95%); /* Slightly dims the box on hover regardless of mode */
    }}

    .center-btn {{
        max-width: 400px;
        margin: auto;
    }}

    /* Makes the sidebar background dynamic based on Streamlit settings */
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-background-color);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# -----------------------------
# 🍳 Render Result (FIXED)
# -----------------------------
def render_recipe_result(result: RecipeResult, language: str, show_raw_output: bool):
    is_rtl = language == "Arabic"
    parsed = result.parsed

    st.markdown('<div class="app-container">', unsafe_allow_html=True)

    st.markdown(f'<div class="recipe-title">🍳 {parsed.title}</div>', unsafe_allow_html=True)

    # Stats
    stats_html = f"""
    <div class="stats-container">
        <div class="stat-box">⏱️ {parsed.estimated_time or "N/A"}</div>
        <div class="stat-box">🔥 {parsed.estimated_calories or "N/A"}</div>
        <div class="stat-box">💰 {parsed.estimated_cost or "N/A"}</div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)

    # Ingredients
    if parsed.ingredients:
        st.markdown('<div class="section-header">🥘 Ingredients</div>', unsafe_allow_html=True)
        html = "".join([f'<div class="item">✓ {i}</div>' for i in parsed.ingredients])
        st.markdown(html, unsafe_allow_html=True)

    # Steps
    if parsed.steps:
        st.markdown('<div class="section-header">👨‍🍳 Steps</div>', unsafe_allow_html=True)
        html = "".join([f'<div class="item">{idx+1}. {s}</div>' for idx, s in enumerate(parsed.steps)])
        st.markdown(html, unsafe_allow_html=True)

    # Alternatives
    if parsed.alternatives:
        st.markdown('<div class="section-header">🔄 Alternatives</div>', unsafe_allow_html=True)
        html = "".join([f'<div class="item">→ {a}</div>' for a in parsed.alternatives])
        st.markdown(html, unsafe_allow_html=True)

    if show_raw_output:
        st.markdown("### Raw Output")
        st.code(result.raw)

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# 🧭 Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    language = st.selectbox("🌐 Language", ["Arabic", "English"])
    is_rtl = language == "Arabic"

    provider = st.selectbox("🤖 Provider", ["openai", "huggingface", "openrouter"])

    api_key = st.text_input("🔑 API Key", type="password")

    mode = st.selectbox("🎯 Mode", ["strict", "natural", "creative"], index=1)

    show_raw_output = st.checkbox("Show raw output")



# Apply styles
apply_custom_styles(is_rtl)

# -----------------------------
# 🧾 Header
# -----------------------------
st.markdown("""
<div style="text-align:center">
<h1 style="color:#FF6B6B;">🍴 AI Recipe Generator</h1>
<p>Generate recipes with AI ✨</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# 📝 Input
# -----------------------------
st.markdown("### 📝 Enter Ingredients")

ingredients = st.text_area(
    "ingredients",
    height=150,
    placeholder="دجاج، طماطم، ثوم..." if is_rtl else "chicken, tomato, garlic...",
    label_visibility="collapsed"
)

st.markdown('<div class="center-btn">', unsafe_allow_html=True)
generate = st.button("🔥 Generate Recipe", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# 🚀 Generate
# -----------------------------
if generate:
    if not ingredients.strip():
        st.error("Please enter ingredients")
    else:
        with st.spinner("Generating..."):
            try:
                orchestrator = Orchestrator(
                    provider_name=provider,
                    api_key=api_key or None
                )

                result = orchestrator.generate_recipe(
                    ingredients,
                    language=language,
                    mode=mode
                )

                st.markdown("---")
                render_recipe_result(result, language, show_raw_output)

            except Exception as e:
                st.error(str(e))