import base64
import requests
from PIL import Image
import io
import json
import logging
import json
import pandas as pd
import re


IMAGE_ANALYSES_KEY = "Image Analyses"
# Configure logging
logging.basicConfig(level=logging.INFO)

import os
api_key = os.environ.get("OPENAI_API_KEY")

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
    "data/competitor/image1.jpeg",
    "data/competitor/image2.jpeg",
    "data/competitor/image3.jpeg",
    "data/competitor/image4.jpeg",
    "data/competitor/image5.jpeg",
    "data/competitor/image6.jpeg"
]

# Headers for the OpenAI API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Competitor information (context for analysis)
competitor_information = """
The competitor is a leading brand in the digital marketing space known for its consistent visual branding and innovative designs on social media. They target a tech-savvy audience aged 20-35 with a focus on modern aesthetics, engaging storytelling, and minimalist yet powerful branding.
"""

system_message = """
Analyze the branding, content marketing, and social media marketing effectiveness of a company for the provided Instagram post image.
Evaluate it based on the following criteria and return a detailed JSON structure. Each criterion should have an individual score (0-10), and the total score for the category should be the average of its criteria.
Give 9 or above only when it's extraordinary. Industry standard 7-8
### Categories and Definitions:

#### Branding:
- **Logo Placement**: Is the logo perfectly sized, clearly visible, and well-positioned without being intrusive?
- **Brand Colors**: Are brand colors used consistently and without deviations?
- **Typography**: Are the fonts aligned with the brand identity, consistent in style, and visually appealing?
- **Brand Identity**: Does the post effectively reflect the brand's unique persona and messaging?
- **Visual Hierarchy**: Are key elements prioritized effectively to guide the viewer’s attention?
- **Template Consistency**: Are templates consistent with previous posts, reflecting a uniform design approach?
- **Messaging Alignment**: Is the brand messaging clear, consistent, and reflective of the brand's tone?
- **Subtle Branding**: Does the branding strike the right balance (not overly subtle or excessive)?
- **Overbranding**: Does the post avoid overwhelming and distracting brand elements?
- **Creative Variations**: Are there innovative and creative design variations in the post?

#### Content Marketing:
- **Content Visibility**: Is the primary content clear and highlighted effectively?
- **Engagement Cues**: Are clear and compelling calls-to-action (CTAs) present and engaging?
- **Information Overload**: Does the post avoid over-saturated visuals or excessive text?
- **Storytelling**: Does the post convey a relevant and engaging narrative that resonates with the audience?
- **Content Variety**: Are the posts diverse and free of monotonous or repetitive elements?
- **Typography Consistency**: Is the typography visually attractive and consistent throughout the design?
- **Aesthetic Coherence**: Do all elements harmonize to create a visually appealing composition?
- **Content Relevance**: Is the content relevant to the brand and its target audience?
- **Stock Elements**: Does the design avoid excessive use of generic or stock imagery?

#### Social Media Marketing:
- **Font Size**: Are fonts appropriately sized and legible on various screen sizes?
- **Visibility of Text**: Is the text easy to read, with proper contrast, placement, and spacing?
- **Logo Placement**: Does the logo placement avoid disrupting the design's aesthetic appeal?
- **Consistency**: Does the post maintain design cohesion across elements?
- **Alignment**: Are elements aligned professionally, creating a balanced and clean layout?
- **Aesthetic Appeal**: Is the overall design visually engaging and suitable for the platform?
- **Brand Elements**: Are brand assets (like logos, icons, or visuals) used effectively and sparingly?
- **Repetitiveness**: Does the design avoid repetitive themes and offer fresh creative ideas?

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

# Function to request analysis from OpenAI API
def request_analysis(system_message, user_message, model="gpt-4o-mini", max_tokens=1500):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": max_tokens
    }
    logging.debug(f"Payload Sent: {json.dumps(payload, indent=4)}")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

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
    user_message = f"""
    Company Information: {competitor_information}
    Analyze the Instagram post with dimensions {width}x{height} pixels. Image data: {base64_image}
    """

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
with open("Output File/json/competitor_analysis.json", "w") as f:
    json.dump(output_structure, f, indent=4)

logging.info("Analysis completed and saved to competitor_analysis.json")


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
json_file_path = "Output File/json/competitor_analysis.json"  # Input JSON file
excel_file_path = "Output File/excel/competitor_analysis.xlsx"  # Output Excel file
json_to_excel(json_file_path, excel_file_path)
