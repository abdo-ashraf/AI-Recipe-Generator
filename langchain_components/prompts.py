from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = """You are a helpful assistant that generates clear, concise Arabic or English recipe instructions.
Output must follow this format exactly for the final parser step:
---RECIPE-START---
Title: <short recipe title>
Language: <Arabic|English>
Ingredients:
- item1
- item2
Steps:
1. step one
Estimated time: <minutes> minutes
Estimated calories: <number> kcal
Estimated cost: <currency> <number>
Alternatives:
- ingredient -> alternative suggestion (brief)
---RECIPE-END---

Be concise and prefer short bullet lists. If user supplies Arabic ingredients, prefer Arabic output."""

RECIPE_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template(
        "User ingredients:\n{ingredients}\n\n"
        "Generate a recipe using the system instructions. Provide a short title, ingredients list, steps, "
        "estimated time in minutes, estimated calories, estimated cost in local currency (approximate), "
        "and short alternatives for expensive or uncommon ingredients."
    )
])
