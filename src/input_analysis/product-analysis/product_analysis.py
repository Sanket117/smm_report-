import base64
import requests
from PIL import Image
import io
import json
import logging
import json
import pandas as pd
import re

# Define constants
API_URL = "https://api.openai.com/v1/chat/completions"
IMAGE_ANALYSES_KEY = "Image Analyses"
import os
api_key = os.environ.get("OPENAI_API_KEY")
# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to encode the image to base64
def encode_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((800, 800))  # Resize image
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return encoded_image
    except Exception as e:
        logging.error(f"Failed to encode image {image_path}: {e}")
        return None

# Function to get image dimensions
def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            return img.size  # returns (width, height)
    except Exception as e:
        logging.error(f"Failed to get dimensions for image {image_path}: {e}")
        return (0, 0)

# Image paths for analysis
image_paths = [
    "data/product/image1.jpeg",
    "data/product/image2.jpeg",
    "data/product/image3.jpeg",
    "data/product/image4.jpeg",
    "data/product/image5.jpeg",
    "data/product/image6.jpeg"
]

# Headers for the OpenAI API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# System Message for Brutal Analysis
system_message = """
Analyze the branding, content marketing, and social media marketing effectiveness of a company for the provided Instagram post image.
Evaluate it with extreme scrutiny, judging harshly and penalizing even minor mistakes or deviations. Scores (0-10) should reflect an unforgiving critique.
A score of 10 should be nearly unattainable, and anything below basic industry standards should score no more than 5. BUT GIVE GOOD SCORE WHEREVER THEY REALLY REALLY DESERVE IT.
The final evaluation must highlight deficiencies prominently, even if they appear minor.

### Categories and Criteria:
#### Branding:
- **Logo Usage**: Penalize heavily if the logo is not perfectly sized, clearly visible, or appropriately placed.
- **Brand Colors**: Deduct points for any deviations or inconsistencies in brand colors.
- **Typography**: Strictly penalize if fonts do not align with the brand identity or lack consistency.
- **Brand Identity**: Judge if the design fails to reflect the unique persona of the brand.
- **Visual Hierarchy**: Critique poor prioritization of key elements, even slightly.
- **Template Consistency**: Penalize mismatched templates or lack of a uniform design approach.
- **Messaging Alignment**: Deduct heavily for vague or inconsistent brand messaging.
- **Subtle Branding**: Punish overly subtle or excessive branding.
- **Overbranding**: Penalize for overwhelming, distracting brand elements.
- **Variations**: Critique lack of variety or creative innovation in the post.

#### Content Marketing:
- **Content Visibility**: Penalize cluttered designs or poorly highlighted content.
- **Engagement Cues**: Harshly judge unclear or missing calls-to-action.
- **Information Overload**: Deduct for over-saturated visuals or excessive text.
- **Storytelling**: Penalize weak, unengaging, or irrelevant narratives.
- **Content Variety**: Deduct for monotony or repetition across posts.
- **Typography Consistency**: Penalize for inconsistent or unattractive typography.
- **Aesthetic Coherence**: Heavily penalize jarring or unappealing designs.
- **Content Relevance**: Deduct for off-brand or irrelevant posts.
- **Stock Elements**: Heavily penalize excessive reliance on generic or stock imagery.

#### Social Media Marketing:
- **Font Size**: Penalize unreadable or poorly sized text, even slightly.
- **Visibility of Text**: Deduct for hard-to-read text due to placement or design choices.
- **Logo Placement**: Harshly critique logos that disrupt the aesthetic.
- **Consistency**: Deduct for designs that lack cohesion or consistency.
- **Alignment**: Penalize for poorly aligned elements or uneven layouts.
- **Aesthetic Appeal**: Heavily penalize designs that lack visual allure or professionalism.
- **Brand Elements**: Critique insufficient or overused brand assets.
- **Repetitiveness**: Harshly penalize repetitive themes or lack of creative diversity.

### Output JSON Format:
### Only return the following format strictly

{
    "Branding Score": total_avg_score, explanation.
    "criteria_name": score, explanation.
    "criteria_name": score, explanation.

    "Content Marketing Score": total_avg_score, explanation.
    "criteria_name": score, explanation.
    "criteria_name": score, explanation.

    "Social Media Marketing Score": total_avg_score, explanation.
    "criteria_name": score, explanation.
    "criteria_name": score, explanation.
}
"""

# Example product information string
product_information = "This product is an eco-friendly, high-performance water bottle designed to keep beverages cold for up to 24 hours. Made with BPA-free materials, it features a sleek design with a customizable logo space."

# Function to request analysis from OpenAI API
def request_analysis(system_message, user_message, model="gpt-4o-mini", max_tokens=1500):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{user_message} Product Information: {product_information}"}
        ],
        "max_tokens": max_tokens
    }
    logging.debug(f"Payload Sent: {json.dumps(payload, indent=4)}")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Unexpected response format")
        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            logging.debug(f"Raw Response: {response.text}")
            return "Error parsing the response."
    else:
        logging.error(f"API Error: {response.status_code}, {response.text}")
        return "Error with the API request."

# Initialize structured output for the analyses
output_structure = {
    IMAGE_ANALYSES_KEY: []
}

# Loop through each image for analysis
for image_path in image_paths:
    base64_image = encode_image(image_path)
    if not base64_image:
        output_structure[IMAGE_ANALYSES_KEY].append({
            "Image": image_path,
            "Analysis": "Failed to encode image."
        })
        continue

    width, height = get_image_dimensions(image_path)
    user_message = f"Analyze the Instagram post with dimensions {width}x{height} pixels. Image data: {base64_image}"

    try:
        analysis_result = request_analysis(system_message, user_message)
        try:
            # Parse result and ensure it matches the required format
            parsed_result = json.loads(analysis_result)
        except json.JSONDecodeError:
            logging.warning(f"Response not in expected JSON format for {image_path}: {analysis_result}")
            parsed_result = {"Raw Response": analysis_result}

        output_structure[IMAGE_ANALYSES_KEY].append({
            "Image": image_path,
            "Analysis": parsed_result
        })
    except Exception as err:
        logging.error(f"Error analyzing image {image_path}: {err}")
        output_structure[IMAGE_ANALYSES_KEY].append({
            "Image": image_path,
            "Analysis": "Error analyzing the image."
        })

# Write structured output to file
with open("Output File/json/product_analysis.json", "w") as f:
    json.dump(output_structure, f, indent=4)


logging.info("Analysis completed and saved to product_analysis.json")


def json_to_excel(json_file, excel_file):
    """
    Parse the JSON file and convert it to an Excel file with structured scores and raw JSON responses.

    Args:
        json_file (str): Path to the input JSON file.
        excel_file (str): Path to the output Excel file.
    """
    # Load JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Prepare a list to hold structured data
    structured_data = []

    # Regex patterns to extract scores and criteria
    score_pattern = r'"([a-zA-Z\s]+)":\s*(\d+),'  # Matches "Criteria Name": Score,

    # Iterate over "Image Analyses" entries
    for analysis in data.get("Image Analyses", []):
        # Extract image name
        image = analysis.get("Image", "Unknown")

        # Extract raw response
        raw_response = analysis.get("Analysis", {}).get("Raw Response", "")

        # Dictionary to hold extracted data for the image
        image_data = {"Image": image, "Raw JSON Response": raw_response}

        # Extract criteria and scores using regex
        matches = re.findall(score_pattern, raw_response)
        for criterion, score in matches:
            image_data[criterion.strip()] = int(score)  # Add criteria as columns

        # Append image data to structured list
        structured_data.append(image_data)

    # Convert structured data to DataFrame
    df = pd.DataFrame(structured_data)

    # Write DataFrame to Excel
    df.to_excel(excel_file, index=False)
    print(f"Data successfully written to {excel_file}")

# Example usage
json_file_path = "Output File/json/product_analysis.json"  # Input JSON file
excel_file_path = "Output File/excel/product_analysis.xlsx"  # Output Excel file
json_to_excel(json_file_path, excel_file_path)
