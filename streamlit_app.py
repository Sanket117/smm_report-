import streamlit as st
from PIL import Image
import os
import subprocess
import time

# Constants for file paths and MIME types
PDF_MIME_TYPE = "application/pdf"
BRAND_MARKETING = "data/reports/template_PDF/brand marketing.pdf"
CONTENT_MARKETING = "data/reports/template_PDF/content marketing.pdf"
SOCIAL_MEDIA_MARKETING = "data/reports/template_PDF/social media marketing.pdf"
PRODUCT_IMAGES_DIR = "data/product"
COMPETITOR_IMAGES_DIR = "data/competitor"
REPORT = "src/Report/report.pdf"
STATUS_FILE = "src/Report/status.txt"  # Path to the status file

# Ensure directories for saving images exist
os.makedirs(PRODUCT_IMAGES_DIR, exist_ok=True)
os.makedirs(COMPETITOR_IMAGES_DIR, exist_ok=True)

# Status checker function
def check_status_file(timeout=600, interval=5):
    """Monitor the status.txt file for completion or errors."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                status = f.read().strip()
                if status == "done":
                    return "success"
                elif status.startswith("error"):
                    return status
        time.sleep(interval)
    return "timeout"

# Initialize session state variables to track process
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "analysis_in_progress" not in st.session_state:
    st.session_state.analysis_in_progress = False

# Streamlit Title and File Upload
st.title("Product vs Competitor Image Analysis")

# Company Name Input
company_name = st.text_input(
    "Company Name",
    placeholder="Enter the company name..."
)

st.subheader("Upload 6 Product Images and Provide Description")
product_images = st.file_uploader(
    "Upload Product Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key="product"
)
about_product = st.text_area(
    "About Product",
    placeholder="Enter a brief description about the product...",
    height=80
)

st.subheader("Upload 6 Competitor Images and Provide Description")
competitor_images = st.file_uploader(
    "Upload Competitor Images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key="competitor"
)
about_competitor = st.text_area(
    "About Competitor",
    placeholder="Enter a brief description about the competitor...",
    height=80
)

# Validation for Image Count
if product_images and competitor_images:
    if len(product_images) == 6 and len(competitor_images) == 6:
        st.success("All images uploaded successfully!")
    else:
        st.warning("Please upload exactly 6 images for both products and competitors.")

# Main "Generate" button logic
if st.button("Generate"):
    # Only proceed if report hasn't been generated or analysis isn't already in progress
    if not st.session_state.report_generated and not st.session_state.analysis_in_progress:
        if product_images and competitor_images and len(product_images) == 6 and len(competitor_images) == 6:
            if company_name:
                st.session_state.analysis_in_progress = True  # mark as in progress
                st.subheader("Product Images vs Competitor Images")

                # Save images to respective directories
                for idx, img_file in enumerate(product_images):
                    img = Image.open(img_file)
                    if img.mode == "RGBA":
                        img = img.convert("RGB")
                    img.save(os.path.join(PRODUCT_IMAGES_DIR, f"image{idx + 1}.jpeg"), "JPEG")

                for idx, img_file in enumerate(competitor_images):
                    img = Image.open(img_file)
                    if img.mode == "RGBA":
                        img = img.convert("RGB")
                    img.save(os.path.join(COMPETITOR_IMAGES_DIR, f"image{idx + 1}.jpeg"), "JPEG")

                try:
                    # Initialize status file with "pending"
                    with open(STATUS_FILE, "w") as f:
                        f.write("pending")

                    # Execute the analysis script asynchronously
                    subprocess.Popen(['python', 'src/analysis.py', company_name])

                    # Monitor the status file
                    st.info("Running analysis. Please wait...")
                    status = check_status_file()

                    if status == "success":
                        st.success("Analysis completed successfully!")
                        st.session_state.report_generated = True  # mark as generated

                        # Download Buttons for Generated PDF Reports
                        for report_name, label in [
                            (BRAND_MARKETING, f"{company_name} Brand Marketing Report"),
                            (CONTENT_MARKETING, f"{company_name} Content Marketing Report"),
                            (SOCIAL_MEDIA_MARKETING, f"{company_name} Social Media Marketing Report")
                        ]:
                            if os.path.exists(report_name):
                                with open(report_name, "rb") as report_file:
                                    st.download_button(
                                        label=f"Download {label}",
                                        data=report_file,
                                        file_name=f"{company_name} {label}.pdf",
                                        mime=PDF_MIME_TYPE
                                    )
                            else:
                                st.error(f"{report_name} not found. Please generate the report first.")
                        
                        # For the custom report
                        custom_report_name = f"{company_name} report.pdf"
                        if os.path.exists(REPORT):
                            with open(REPORT, "rb") as report_file:
                                st.download_button(
                                    label=f"Download {company_name} Report",
                                    data=report_file,
                                    file_name=custom_report_name,
                                    mime=PDF_MIME_TYPE
                                )
                        else:
                            st.error(f"{REPORT} not found. Please generate the report first.")
                    elif status == "timeout":
                        st.error("Analysis timed out. Please try again.")
                    else:
                        st.error(f"Analysis script failed: {status}")
                except Exception as e:
                    st.error(f"Error running analysis script: {e}")
                finally:
                    st.session_state.analysis_in_progress = False  # reset the flag
            else:
                st.warning("Please enter your company name.")
        else:
            st.warning("Please upload exactly 6 images for both products and competitors before generating.")
    else:
        st.info("Report has already been generated for this session.")
