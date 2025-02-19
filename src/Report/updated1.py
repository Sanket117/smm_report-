import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

def create_overlay_pdf(text, x, y, output_overlay_pdf, page_width, page_height, max_width):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Set initial font size
    font_size = 44  # Larger font size to start with
    can.setFont("Helvetica-Bold", font_size)
    can.setFillColorRGB(0, 0, 0)  # Black text

    # Measure the text width
    text_width = can.stringWidth(text, "Helvetica-Bold", font_size)
    
    # If the text is too wide, reduce font size to fit within the max_width
    if text_width > max_width:
        font_size = 18  # Reduce font size if necessary
        can.setFont("Helvetica-Bold", font_size)
        text_width = can.stringWidth(text, "Helvetica-Bold", font_size)

    # Convert page_width to float if it's a Decimal
    page_width = float(page_width)  # Convert to float to avoid TypeError

    # Dynamically calculate the x-coordinate to center the text
    x_coordinate = (page_width - text_width) / 2  # Center the text horizontally

    # Draw the string at the calculated position
    can.drawString(x_coordinate, y, text)
    can.save()

    packet.seek(0)
    with open(output_overlay_pdf, "wb") as overlay_file:
        overlay_file.write(packet.getvalue())

def merge_pdfs(input_pdf, overlay_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    overlay = PdfReader(overlay_pdf)
    writer = PdfWriter()

    # Apply the overlay to the first page
    original_page = reader.pages[0]
    original_page.merge_page(overlay.pages[0])

    writer.add_page(original_page)

    # Add the remaining pages without the overlay
    for page_num in range(1, len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    # Retrieve company_name from command-line argument or use default
    if len(sys.argv) > 1:
        company_name = sys.argv[1]
    else:
        company_name = "Default_Company"

    input_pdf_path = "data/reports/report_stats/1.pdf"
    overlay_pdf_path = "src/Report/overlay_test.pdf"
    output_pdf_path = "src/Report/1updated.pdf"

    # Load the original PDF to get its dimensions
    reader = PdfReader(input_pdf_path)
    original_page = reader.pages[0]
    page_width = original_page.mediabox.width
    page_height = original_page.mediabox.height

    # Start with conservative coordinates and adjust as needed
    x_coordinate = 800  # Adjust as needed
    y_coordinate = 600  # Adjust as needed
    max_width = 500  # Maximum width for the text

    # Step 1: Create the overlay PDF with the same size as the original page
    create_overlay_pdf(company_name, x_coordinate, y_coordinate, overlay_pdf_path, page_width, page_height, max_width)
    
    # Step 2: Merge the overlay with the original PDF
    merge_pdfs(input_pdf_path, overlay_pdf_path, output_pdf_path)

    print(f"Generated PDF saved as {output_pdf_path} with company name: {company_name}")













