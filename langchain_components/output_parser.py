import re
from typing import Dict


def parse_recipe_output(text: str) -> Dict:
    # Attempt to find the section between the markers
    m = re.search(r"---RECIPE-START---(.*)---RECIPE-END---", text, re.S)
    body = m.group(1).strip() if m else text

    # Simple extraction helpers
    def extract_field(tag: str) -> str:
        pat = rf"{tag}:\s*(.*)"
        mm = re.search(pat, body)
        return mm.group(1).strip() if mm else ""

    def extract_list(section: str) -> list:
        pat = rf"{section}:\s*(.*?)\n\n"
        mm = re.search(pat, body, re.S)
        if not mm:
            # fallback: lines starting with -
            return [l.strip()[2:].strip() for l in body.splitlines() if l.strip().startswith("-")]
        items = [line.strip()[2:].strip() for line in mm.group(1).splitlines() if line.strip().startswith("-")]
        return items

    title = extract_field("Title")
    lang = extract_field("Language")
    time = extract_field("Estimated time")
    calories = extract_field("Estimated calories")
    cost = extract_field("Estimated cost")
    ingredients = extract_list("Ingredients")
    steps = []
    # steps: capture numbered steps
    steps_matches = re.findall(r"^\s*\d+\.\s*(.*)$", body, re.M)
    if steps_matches:
        steps = [s.strip() for s in steps_matches]

    return {
        "title": title,
        "language": lang,
        "time": time,
        "calories": calories,
        "cost": cost,
        "ingredients": ingredients,
        "steps": steps,
    }
