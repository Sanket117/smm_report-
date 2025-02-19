import pandas as pd
import os
import re  # For sanitizing the filenames

# Define file paths
product_analysis_path = "Output File/excel/product_analysis.xlsx"
competitor_analysis_path = "Output File/excel/competitor_analysis.xlsx"
top_3_df_path = "Output File/excel/top_3_sd_results.xlsx"

# Read the data from Excel files
product_data = pd.read_excel(product_analysis_path)
competitor_data = pd.read_excel(competitor_analysis_path)
top_3_df = pd.read_excel(top_3_df_path)

# Create directory D if not exists
output_dir = "data/top_3_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Check columns to make sure we are accessing the correct data
print("Product Data Columns:", product_data.columns)
print("Competitor Data Columns:", competitor_data.columns)

# Function to sanitize filenames (remove any invalid characters)
def sanitize_filename(name):
    # Replace any character that's not alphanumeric, space, or underscore with an underscore
    return re.sub(r'[^\w\s-]', '_', name).strip().replace(' ', '_')

# Process Product Image Names
for image_name in top_3_df['Product_Image_Name']:
    # Sanitize the image name to avoid invalid filename characters
    sanitized_image_name = sanitize_filename(image_name)

    # Fetch raw JSON response for the image in Product data by matching 'Image' column
    product_response = product_data.loc[product_data['Image'] == image_name, 'Raw JSON Response'].values
    if len(product_response) > 0:
        raw_response = product_response[0]
        if raw_response:  # Check if the response is not empty
            with open(f"{output_dir}/{sanitized_image_name}.txt", 'w') as file:
                file.write(raw_response)  # Write raw response as text
            print(f"Saved Raw Text for Product image: {sanitized_image_name}")
        else:
            print(f"Empty Raw JSON Response for Product image: {sanitized_image_name}")
    else:
        print(f"Product image name '{image_name}' not found.")

# Process Competitor Image Names
for image_name in top_3_df['Competitor_Image_Name']:
    # Sanitize the image name to avoid invalid filename characters
    sanitized_image_name = sanitize_filename(image_name)

    # Fetch raw JSON response for the image in Competitor data by matching 'Image' column
    competitor_response = competitor_data.loc[competitor_data['Image'] == image_name, 'Raw JSON Response'].values
    if len(competitor_response) > 0:
        raw_response = competitor_response[0]
        if raw_response:  # Check if the response is not empty
            with open(f"{output_dir}/{sanitized_image_name}.txt", 'w') as file:
                file.write(raw_response)  # Write raw response as text
            print(f"Saved Raw Text for Competitor image: {sanitized_image_name}")
        else:
            print(f"Empty Raw JSON Response for Competitor image: {sanitized_image_name}")
    else:
        print(f"Competitor image name '{image_name}' not found.")
