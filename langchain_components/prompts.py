from langchain_core.prompts import PromptTemplate

_BASE_PROMPT = """
You are a helpful assistant that generates structured recipe data.

Mode instructions:
{mode_instruction}

Output format instructions:
{format_instructions}

Rules:
- Be concise
- Keep values realistic
- Ensure valid JSON output
- Do not include any text outside the JSON
- PROVIDE THE ANSWER IN {language}

User request:
{user_input}
"""

RECIPE_PROMPT_TEMPLATE = PromptTemplate(
    template=_BASE_PROMPT,
    input_variables=["user_input", "format_instructions", "mode_instruction", "language"]
)

