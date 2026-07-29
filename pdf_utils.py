import fitz  # PyMuPDF


def extract_pages(pdf_path, start_page, end_page):

    pdf = fitz.open(pdf_path)

    extracted_text = ""

    # PyMuPDF starts counting pages from 0
    for page_num in range(start_page - 1, end_page):

        page = pdf.load_page(page_num)

        blocks = page.get_text("blocks")

    for block in blocks:
        print(block)  # Extract text in blocks for better formatting

    pdf.close()

    return extracted_text