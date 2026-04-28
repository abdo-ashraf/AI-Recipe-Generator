from langchain_core.prompts import PromptTemplate

_BASE_PROMPT = """
You are a helpful assistant that generates structured recipe data in JSON format.

Mode instructions:
{mode_instruction}

Output format instructions:
{format_instructions}

Rules:
- Be concise and precise
- Keep values realistic
- Output ONLY valid JSON
- Do NOT include any text outside the JSON
- For list fields (ingredients, steps, alternatives): provide items separated by commas
- PROVIDE THE ANSWER IN {language}

User request:
{user_input}
"""

RECIPE_PROMPT_TEMPLATE = PromptTemplate(
    template=_BASE_PROMPT,
    input_variables=["user_input", "format_instructions", "mode_instruction", "language"]
)


