from enum import Enum
from typing import Dict, Any


class Mode(str, Enum):
    STRICT = "strict"
    NATURAL = "natural"
    CREATIVE = "creative"


PRESETS: Dict[str, Dict[str, Any]] = {
    "strict": {
        "temperature": 0.2,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 1024,
    },
    "natural": {
        "temperature": 0.5,
        "top_p": 0.95,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.1,
        "max_tokens": 1024,
    },
    "creative": {
        "temperature": 0.9,
        "top_p": 0.85,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
        "max_tokens": 1024,
    },
}


MODE_INSTRUCTIONS: Dict[str, str] = {
    "strict": (
        "You are on a strict recipe generation mode."
        "Follow the format strictly. Be precise and factual.\n"
        "Do not add extra descriptions, storytelling, or assumptions.\n"
        "Keep ingredients and steps minimal and realistic."
    ),
    "natural": (
        "You are on a natural recipe generation mode."
        "Follow the format strictly. Be clear and helpful.\n"
        "Use natural phrasing while keeping things concise.\n"
        "Ensure the recipe is practical and easy to follow."
    ),
    "creative": (
        "You are on a creative recipe generation mode."
        "Follow the format strictly. Be creative but still realistic.\n"
        "You may enhance the recipe with interesting variations, flavors, or presentation ideas.\n"
        "Keep the structure intact but make the recipe more appealing."
    ),
}
