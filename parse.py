from dotenv import load_dotenv
load_dotenv()                       # ① single call is enough

import os
from openai import OpenAI
from typing import List


token = os.getenv("GITHUB_TOKEN")
if not token:
    raise RuntimeError("GITHUB_TOKEN not found in environment (.env or secrets)")

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=token,
)

MODEL_NAME = "openai/gpt-4.1"


TEMPLATE = (
    "You are a strict data parser. Extract only the exact information described below "
    "from the provided HTML/text.\n\n"
    "CONTENT:\n{dom_content}\n\n"
    "INSTRUCTIONS:\n"
    "1. Extract the information that matches this description exactly: {parse_description}.\n"
    "2. Respond **only** with valid CSV — a single header row followed by data rows.\n"
    "3. If nothing matches, respond with the header row only.\n"
    "4. Do NOT add explanations, markdown, or extra text.\n\n"
    "RESPONSE FORMAT:\n"
    "CSV only. No markdown fences. No blank lines before or after."
    "Each row should be a single line, with values separated by ';:;'.\n"
    "Row must be separated by '\n'"
    "And if a Particular data is not available, then it should be replace with ''.\n\n"
)


def parse_with_custom_model(dom_chunks: List[str], parse_description: str):
   
    header = None
    data_rows = []

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = TEMPLATE.format(dom_content=chunk, parse_description=parse_description)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        csv_text = response.choices[0].message.content
        print(f"Parsed batch {i} of {len(dom_chunks)}")

        lines = [ln.strip("\ufeff").strip() for ln in csv_text.splitlines() if ln.strip()]
        if not lines:
            continue

   
        if header is None:
            header = lines[0]

        start_idx = 1 if lines[0] == header else 0
        data_rows.extend(lines[start_idx:])


    if header is None:
        raise ValueError("Model returned no CSV header in any chunk.")

    final_csv = "\n".join([header, *data_rows])
    with open('parsed_output.csv', 'w') as f:
        f.write(final_csv)
    # return final_csv

