import base64
import os
from pathlib import Path

import anthropic

DEFAULT_MODEL = os.environ.get("CARD_SCAN_MODEL", "claude-sonnet-5")

SYSTEM_PROMPT = """You are extracting structured data from a photo of a sports trading card.
Read the front (and back, if provided) carefully. Card layout conventions:
- Card number is usually a small number preceded by '#' in a corner.
- Serial numbers (for limited/parallel cards) are printed in a format like '12/99' or
  '045/150', often on the back or in a small strip on the front, and are the field most
  likely to be misread — look closely before answering.
- Year is the card's print year, not necessarily a player stat year printed elsewhere.
- parallel_insert_type is the parallel/insert name if visible (e.g. 'Refractor', 'Gold
  Parallel', 'Base') or 'Base' if it's a standard base card.
- notable_flags should note visible autograph or memorabilia/relic patches, else 'none'.

If a field is not present on the card (e.g. no serial number on a base card), return
value 'N/A' with confidence 1.0. If a field is present but you are not confident you
read it correctly, still provide your best-guess value but lower the confidence score
accordingly (below 0.85 for anything you're genuinely unsure about, especially serial
numbers and text obscured by glare or foil).
"""

FIELD_NAMES = [
    "player",
    "team",
    "year",
    "set",
    "card_number",
    "serial_number",
    "parallel_insert_type",
    "notable_flags",
]

RECORD_CARD_FIELDS_TOOL = {
    "name": "record_card_fields",
    "description": "Record the extracted structured fields for a sports card photo.",
    "input_schema": {
        "type": "object",
        "properties": {
            name: {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "confidence": {
                        "type": "number",
                        "description": "0.0-1.0 confidence that value is correct",
                    },
                },
                "required": ["value", "confidence"],
            }
            for name in FIELD_NAMES
        },
        "required": FIELD_NAMES,
    },
}


def _image_block(path: str) -> dict:
    data = Path(path).read_bytes()
    media_type = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": base64.standard_b64encode(data).decode("utf-8"),
        },
    }


class ExtractionError(RuntimeError):
    pass


def extract_card_fields(
    image_path_front: str, image_path_back: str | None, model: str = DEFAULT_MODEL
) -> tuple[dict, dict]:
    """Returns (fields_dict, raw_response_dict). Raises ExtractionError on failure."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ExtractionError("ANTHROPIC_API_KEY is not set")

    client = anthropic.Anthropic(api_key=api_key)

    content = [_image_block(image_path_front)]
    text = "Front of card shown above."
    if image_path_back:
        content.append(_image_block(image_path_back))
        text = "Front of card shown first, back of card shown second."
    content.append({"type": "text", "text": text})

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=[RECORD_CARD_FIELDS_TOOL],
            tool_choice={"type": "tool", "name": "record_card_fields"},
            messages=[{"role": "user", "content": content}],
        )
    except anthropic.APIError as exc:
        raise ExtractionError(str(exc)) from exc

    tool_use_block = next(
        (block for block in response.content if block.type == "tool_use"), None
    )
    if tool_use_block is None:
        raise ExtractionError("model did not return a tool_use block")

    fields = tool_use_block.input
    raw_response = response.model_dump()
    return fields, raw_response
