from pdf_utils import extract_pages

text = extract_pages(
    "hazcard.pdf",
    53,
    54
)

print(text)