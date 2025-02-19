import os
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from screeninfo import get_monitors
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

def get_screen_size():
    """Get the primary monitor screen size."""
    try:
        monitor = get_monitors()[0]  # Get primary monitor
        screen_width = monitor.width
        screen_height = monitor.height
        return screen_width, int(screen_height * 1.5)  # Scale height
    except Exception as e:
        print(f"Error getting screen size: {e}")
    return 1000, 1500  # Default size

def add_padding_to_pdf(input_pdf, output_pdf, padding):
    """Add padding to a PDF file."""
    try:
        reader = PyPDF2.PdfReader(input_pdf)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            original_width = page.mediabox.width
            original_height = page.mediabox.height

            # New dimensions with padding
            new_width = original_width + 2 * padding
            new_height = original_height + 2 * padding

            # Create a new canvas
            packet = canvas.Canvas(output_pdf, pagesize=(new_width, new_height))
            packet.translate(padding, padding)  # Center original content
            packet.save()

            writer.add_page(page)

        with open(output_pdf, "wb") as out_file:
            writer.write(out_file)

        print(f"✅ Padding added: {input_pdf} -> {output_pdf}")

    except Exception as e:
        print(f"⚠️ Error adding padding to {input_pdf}: {e}")

def merge_pdfs(pdf_list, output_path, elongated_files=[], normalize_size=True):
    """Merge multiple PDFs into a single PDF."""
    pdf_merger = PyPDF2.PdfMerger()

    # Resolve absolute paths
    pdf_list = [os.path.abspath(pdf) for pdf in pdf_list]

    for pdf in pdf_list:
        if not os.path.exists(pdf):
            print(f"⚠️ File not found: {pdf}")
            continue

        try:
            if pdf in elongated_files:
                print(f"🔍 Processing elongated file: {pdf}")
                # Add additional elongation logic here if needed
            pdf_merger.append(pdf)
            print(f"✅ Added: {pdf}")
        except Exception as e:
            print(f"⚠️ Could not add {pdf}: {e}")

    try:
        pdf_merger.write(output_path)
        print(f"📄 Merged PDF saved as: {output_path}")
    except Exception as e:
        print(f"Error saving merged PDF: {e}")
    finally:
        pdf_merger.close()

if __name__ == "__main__":
    # List of PDF files to merge
    pdf_files = [
        "src/Report/1updated.pdf",
        "data/reports/report_stats/2.pdf",
        "data/reports/report_stats/3.pdf",
        "data/reports/report_stats/objective.pdf",
        "data/reports/template_PDF/brand marketing.pdf",
        "data/reports/template_PDF/content marketing.pdf",
        "data/reports/template_PDF/social media marketing.pdf",
        "data/reports/report_stats/last.pdf"
    ]

    elongated_pdfs = [
        "data/reports/template_PDF/brand marketing.pdf",
        "data/reports/template_PDF/content marketing.pdf",
        "data/reports/template_PDF/social media marketing.pdf"
    ]

    # Define output directory and strict file name
    output_dir = "src/Report"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_file = os.path.join(output_dir, "report.pdf")  # Enforce strict file name as report.pdf

    # Merge the PDFs and save the result in the specified directory
    merge_pdfs(pdf_files, output_file, elongated_files=elongated_pdfs)



