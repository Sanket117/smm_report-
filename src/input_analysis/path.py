import os

# Define the paths
input_dir = 'data/top_3_images'
output_dir = 'data/output_generated_file'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop over all .txt files in the 'D' folder
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_dir, filename)

        # Read the content of each text file
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Determine if it's a product or competitor
        is_product = 'product' in filename.lower()
        if is_product:
            branding_file = os.path.join(output_dir, 'Product_branding.txt')
            content_marketing_file = os.path.join(output_dir, 'Product_content_marketing.txt')
            smm_file = os.path.join(output_dir, 'Product_smm.txt')
        else:
            branding_file = os.path.join(output_dir, 'Competitor_branding.txt')
            content_marketing_file = os.path.join(output_dir, 'Competitor_content_marketing.txt')
            smm_file = os.path.join(output_dir, 'Competitor_smm.txt')

        # Split the content into lines
        lines = file_content.split('\n')

        # Prepare content variables for each category
        branding_content = []
        content_marketing_content = []
        smm_content = []

        current_category = None

        # Iterate over lines to categorize them based on detected categories
        for line in lines:
            if "Branding" in line:
                current_category = 'Branding'
            elif "Content Marketing" in line:
                current_category = 'Content Marketing'
            elif "Social Media Marketing" in line:
                current_category = 'Social Media Marketing'

            # Append line to the corresponding category
            if current_category == 'Branding':
                branding_content.append(line)
            elif current_category == 'Content Marketing':
                content_marketing_content.append(line)
            elif current_category == 'Social Media Marketing':
                smm_content.append(line)

        # Write the extracted data into their respective files (overwrite the files)
        with open(branding_file, 'w') as bf:  # 'w' mode will overwrite the file
            bf.write('\n'.join(branding_content) + '\n\n')  # Add the new content

        with open(content_marketing_file, 'w') as cmf:  # 'w' mode will overwrite the file
            cmf.write('\n'.join(content_marketing_content) + '\n\n')

        with open(smm_file, 'w') as smf:  # 'w' mode will overwrite the file
            smf.write('\n'.join(smm_content) + '\n\n')

        print(f"Processed {filename} and saved data into {branding_file}, {content_marketing_file}, and {smm_file}")
