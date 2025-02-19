import pandas as pd
import base64
import os
import sys
from playwright.sync_api import sync_playwright
from PIL import Image

def save_html_file(file_name, html_content):
    with open(file_name, 'w') as file:
        file.write(html_content)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Allow user to upload images for logo and product images
logo_image_path = r"src/templates_images/Component 3.png"
# Encode images to base64
logo_base64 = encode_image_to_base64(logo_image_path)
def save_html_file(file_name, html_content):
    with open(file_name, 'w') as file:
        file.write(html_content)

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        return ""
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return ""

# Encode images to base64
def generate_content_marketing_html(product_image_base64_1, competitor_image_base64_1, product_image_base64_2, competitor_image_base64_2, product_image_base64_3, competitor_image_base64_3, donts_html, suggestions_html, company_name):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Marketing Template</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 10%;  /* Increased padding */
            background-color: #fff;
            font-size: 8px;  /* Increased font size */
        }}
        @page {{
            size: A4;
            margin: 15px;  /* Increased margin */
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;  /* Increased padding */
            background-color: #FFFFFF;
            margin-bottom: 15px;  /* Increased margin */
        }}
        .header .logo {{
            height: 30px;  /* Increased logo height */
        }}
        .container {{
            display: flex;
            flex-direction: column;
            padding: 10px;  /* Increased padding */
            flex-grow: 1;
        }}
        h1 {{
            font-family: 'Times New Roman', serif;
            font-size: 24px;  /* Increased font size */
            font-weight: 500;
            line-height: 1.3;
            text-align: left;
            margin-bottom: 20px;  /* Increased bottom margin */
        }}
        h2, p {{
            font-size: 13px;  /* Increased font size */
            font-weight: 400;
            line-height: 1.5;
            color: #000;
        }}
        .gap {{
            font-size: 11px;  /* Increased font size */
            color: rgb(5, 5, 5);
            font-weight: 100;
        }}
        .examples {{
            font-size: 13px;  /* Increased font size */
            color: green;
        }}
        .box-container {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;  /* Increased margin */
        }}
        .wraper {{
            width: 100%;
            height: 220px;  /* Increased height */
            display: flex;
            margin: 10px 0;  /* Increased margin */
            border-radius: 12px;  /* Increased border radius */
            overflow: hidden;
            position: relative;
        }}
        .div-1 {{
            flex: 1;
            background-color: #ecbdbd; /* Pink background */
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .div-2 {{
            flex: 1;
            background-color: #e6f9e6; /* Green background */
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .wraper img {{
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
            border-radius: 8px;
        }}
        .vs-text {{
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            font-size: 18px;  /* Increased font size */
            font-weight: bold;
            color: black;
        }}
        .side-by-side-container {{
            display: flex;
            gap: 40px;  /* Increased gap between boxes */
            margin-top: 50px;  /* Increased top margin */
        }}
        .pink-box, .green-box {{
            flex: 1;
            padding: 20px;  /* Increased padding */
            margin-top: 20px;  /* Increased margin */
            border-radius: 15px;  /* Increased border radius */
            box-sizing: border-box;
            height: auto;
        }}
        .pink-box {{
            background-color: #ecbdbd;
            color: red;
            text-align: start;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }}
        .pink-box h6 {{
            font-size: 14px;  /* Increased font size */
            font-weight: bold;
            margin: 10px 0;  /* Increased margin */
            color: red;
        }}
        .green-box {{
            background-color: #e6f9e6;
            color: green;
            text-align: start;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }}
        .green-box h6 {{
            font-size: 14px;  /* Increased font size */
            font-weight: bold;
            margin: 10px 0;  /* Increased margin */
            color: green;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1><span style="color:red;">Content Marketing</span></h1>
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo">
    </div>
    <div class="container">
        <p>{company_name} should use Content Marketing effectively as the strategic promotion for identity, products, and services across all channels to create loyalty among consumers.</p>
        <p class="gap"><span style="color: red;">Issue/Gap:</span> {company_name}'s current content marketing efforts might not be reaching their full potential. A comprehensive analysis of brand messaging, target audience engagement across channels, and content strategy could reveal opportunities to optimize {company_name}'s marketing approach for greater reach and impact.</p>
    </div>
    <h2 class="examples">Examples:</h2>
    <div class="box-container">
        <div class="wraper">
            <div class="div-1"> 
                <img src="data:image/png;base64,{product_image_base64_1}" alt="Product Image">
            </div>
            <div class="vs-text">V/S</div>
            <div class="div-2">
                <img src="data:image/png;base64,{competitor_image_base64_1}" alt="Competitor Image">
            </div>
        </div>
        <div class="wraper">
            <div class="div-1"> 
                <img src="data:image/png;base64,{product_image_base64_2}" alt="Product Image">
            </div>
            <div class="vs-text">V/S</div>
            <div class="div-2">
                <img src="data:image/png;base64,{competitor_image_base64_2}" alt="Competitor Image">
            </div>
        </div>
        <div class="wraper">
            <div class="div-1"> 
                <img src="data:image/png;base64,{product_image_base64_3}" alt="Product Image">
            </div>
            <div class="vs-text">V/S</div>
            <div class="div-2">
                <img src="data:image/png;base64,{competitor_image_base64_3}" alt="Competitor Image">
            </div>
        </div>
    </div>
    <div class="side-by-side-container">
        <div class="pink-box">
            <h6>Drawbacks in Current Content Marketing</h6>
            <p>{donts_html}</p>
        </div>
        <div class="green-box">
            <h6>How Banao Technologies Can Help</h6>
            <p>{suggestions_html}</p>
        </div>
    </div>
</body>
</html>
"""

# Function to parse "Product_output_cleaned.txt" for Don'ts and Suggestions specific to Content Marketing
def parse_cleaned_file_content_marketing(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    sections = content.split("==================================================")
    for section in sections:
        lines = section.strip().split("\n")
        if lines and "Content Marketing" in lines[0]:
            donts = []
            suggestions = []
            mode = None
            for line in lines[1:]:
                if line.startswith("Don'ts:"):
                    mode = "donts"
                elif line.startswith("Suggestions:"):
                    mode = "suggestions"
                elif mode == "donts" and line.startswith("-"):
                    donts.append(line.lstrip("- "))
                elif mode == "suggestions" and line.startswith("-"):
                    suggestions.append(line.lstrip("- "))
            return "<br>".join(donts), "<br>".join(suggestions)

    return "", ""

# Function to process Content Marketing and generate HTML
def process_content_marketing(data, base_image_dir, output_file, cleaned_file_path, company_name):
    # Filter for Content Marketing category
    content_data = data[data["Category"] == "Content Marketing"]
    
    if content_data.empty:
        print("No Content Marketing data found in the provided Excel file.")
        return
       # Parse Don'ts and Suggestions
    donts_html, suggestions_html = parse_cleaned_file_content_marketing(cleaned_file_path)

    # Ensure there are at least two rows
    if len(content_data) < 3:
         print("Not enough rows for two product and competitor image comparisons.")
         return
    # Get the first record (assuming one Content Marketing entry is needed)
    # Get the first two records (assuming these are needed)
    content_row_1 = content_data.iloc[0]
    content_row_2 = content_data.iloc[1]
    content_row_3 = content_data.iloc[2]

    product_image_path_1 = os.path.join(base_image_dir, content_row_1["Product_Image_Name"])
    competitor_image_path_1 = os.path.join(base_image_dir, content_row_1["Competitor_Image_Name"])

    product_image_path_2 = os.path.join(base_image_dir, content_row_2["Product_Image_Name"])
    competitor_image_path_2 = os.path.join(base_image_dir, content_row_2["Competitor_Image_Name"])

    product_image_path_3 = os.path.join(base_image_dir, content_row_3["Product_Image_Name"])
    competitor_image_path_3 = os.path.join(base_image_dir, content_row_3["Competitor_Image_Name"])

    # Encode images to Base64
    product_image_base64_1 = encode_image_to_base64(product_image_path_1)
    competitor_image_base64_1 = encode_image_to_base64(competitor_image_path_1)

    product_image_base64_2 = encode_image_to_base64(product_image_path_2)
    competitor_image_base64_2 = encode_image_to_base64(competitor_image_path_2)

    # Encode images to Base64
    product_image_base64_3 = encode_image_to_base64(product_image_path_3)
    competitor_image_base64_3 = encode_image_to_base64(competitor_image_path_3)

    # Generate HTML content
    html_content = generate_content_marketing_html(product_image_base64_1, competitor_image_base64_1, product_image_base64_2, competitor_image_base64_2, product_image_base64_3, competitor_image_base64_3, donts_html, suggestions_html, company_name)

    # Save the HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file for Content Marketing has been saved as: {output_file}")

# Main script for Content Marketing
if __name__ == "__main__":
    if len(sys.argv) > 1:
        company_name = sys.argv[1]  # The second argument passed will be the company_name
    else:
        company_name = "Default_Company"  # Default value if no argument is passed
    # Load the Excel file
    file_path = "Output File/excel/top_3_sd_results.xlsx"  # Replace with the path to your Excel file
    data = pd.read_excel(file_path)

    # Set the base directory for images
    base_image_dir = ""  # Replace with the actual directory where your images are stored

    # Path to the cleaned file with Don'ts and Suggestions
    cleaned_file_path = "data/output_generated_file/Product_output_cleaned.txt"
    # Output HTML file
    output_file = "src/templates/content_marketing.html"

    # Generate HTML for Content Marketing
    process_content_marketing(data, base_image_dir, output_file, cleaned_file_path, company_name)

# Force UTF-8 encoding for terminal output
sys.stdout.reconfigure(encoding='utf-8')

def capture_screenshot_with_playwright(html_file_path, screenshot_path):
    """
    Capture a full-page screenshot of the HTML file directly using Playwright.
    """
    try:
        # Launch Playwright in headless mode
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Open the HTML file in the browser
            page.goto(f"file:///{os.path.abspath(html_file_path)}")
            
            # Capture the full-page screenshot
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved: {screenshot_path}")

            browser.close()

    except Exception as e:
        print(f"Error capturing screenshot: {e}")

def convert_png_to_pdf(png_path, company_name):
    """
    Convert a PNG image into a PDF strictly named as 'company_name brand marketing.pdf'
    in the specified folder 'data/reports/template_PDF'.
    """
    try:
        # Set the output folder and ensure it exists
        output_folder = "data/reports/template_PDF"
        os.makedirs(output_folder, exist_ok=True)

        # Create the PDF file name as 'company_name brand marketing.pdf'
        pdf_path = os.path.join(output_folder, "content marketing.pdf") 

        # Convert the PNG to PDF
        img = Image.open(png_path)
        img.convert('RGB').save(pdf_path, "PDF")

        print(f"PDF saved: {pdf_path}")
    except Exception as e:
        print(f"Error converting PNG to PDF: {e}")

if __name__ == "__main__":
    # Paths for demonstration
    html_file_path = "src/templates/content_marketing.html"
    
    # Screenshot saved in the folder: data/reports/template_ss
    screenshot_folder = "data/reports/template_ss"
    os.makedirs(screenshot_folder, exist_ok=True)
    screenshot_path = os.path.join(screenshot_folder, "content_marketing_screenshot.png")

    # Ensure Playwright browsers are installed
    os.system("playwright install")

    # Capture screenshot
    capture_screenshot_with_playwright(html_file_path, screenshot_path)

    # Convert screenshot to PDF with the company name strictly as the filename
    convert_png_to_pdf(screenshot_path, company_name)








