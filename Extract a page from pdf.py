import fitz
print("Extracting text from page 1 of hazcard.pdf")
file_name = "hazcard.pdf"
doc = fitz.open(file_name)

page = doc[6]


blocks = page.get_text("blocks")


for block in blocks:

    x0, y0, x1, y1, text, block_no, block_type = block

    print("----------------")
    print("Position:")
    print(x0, y0, x1, y1)

    print(text)