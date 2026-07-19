import fitz

pdf = fitz.open("hazcard.pdf")

page_number = 84       # example

page = pdf.load_page(page_number)

text = page.get_text()

from openai import OpenAI

client = OpenAI()

prompt = f"""
You are extracting chemical data from CLEAPSS Hazcards.

Extract EVERY chemical on this page.

Return ONLY valid JSON.

Format:

[
  {{
    "name":"",
    "aliases":[],
    "formula":""
  }}
]

Page:

{text}
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role":"user",
            "content":prompt
        }
    ],
    response_format={"type":"json_object"}
)