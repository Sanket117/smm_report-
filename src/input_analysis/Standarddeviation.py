import pandas as pd
import numpy as np

# Load Excel files
product_data = pd.read_excel("Output File/excel/product_analysis.xlsx")
competitor_data = pd.read_excel("Output File/excel/competitor_analysis.xlsx")

# Function to filter criteria based on available columns
def filter_existing_criteria(data, criteria):
    """
    Filters a list of criteria to include only those present in the given DataFrame columns.

    Args:
        data: DataFrame containing the data.
        criteria: List of criteria to filter.

    Returns:
        List of filtered criteria that exist in the DataFrame columns.
    """
    return [criterion for criterion in criteria if criterion in data.columns]

# Define criteria for each category
branding_criteria = [
    "Logo Placement", "Consistency", "Alignment",
    "Brand Colors", "Typography Consistency", "Brand Identity", "Template Consistency"
]
content_marketing_criteria = [
    "Content Visibility", "Engagement Cues", "Storytelling",
    "Aesthetic Coherence", "Content Relevance"
]
social_media_marketing_criteria = [
    "Font Size", "Visibility of Text", "Alignment",
    "Aesthetic Appeal", "Repetitiveness"
]

# Filter criteria based on available columns in the data
branding_criteria_filtered = filter_existing_criteria(product_data, branding_criteria)
content_marketing_criteria_filtered = filter_existing_criteria(product_data, content_marketing_criteria)
social_media_marketing_criteria_filtered = filter_existing_criteria(product_data, social_media_marketing_criteria)

# Helper function to calculate the mean value for a criterion
def calculate_mean_criterion_value(product_data, competitor_data, criterion):
    """
    Calculate the mean of a criterion from both product and competitor data, ignoring NaN values.

    Args:
        product_data: DataFrame containing product data.
        competitor_data: DataFrame containing competitor data.
        criterion: The column name representing the criterion.

    Returns:
        Mean value of the criterion.
    """
    combined_values = np.concatenate([
        product_data[criterion].dropna().values,
        competitor_data[criterion].dropna().values,
    ])
    return np.nanmean(combined_values)

# Helper function to calculate the score differences
def calculate_score_differences(product_scores, competitor_scores, product_data, competitor_data, category_criteria):
    """
    Calculate the score differences, replacing NaN with mean values.

    Args:
        product_scores: Scores of a product post for the criteria.
        competitor_scores: Scores of a competitor post for the criteria.
        product_data: DataFrame containing product data.
        competitor_data: DataFrame containing competitor data.
        category_criteria: List of criteria in the category.

    Returns:
        Array of score differences.
    """
    score_diff = product_scores - competitor_scores
    for k, diff in enumerate(score_diff):
        if np.isnan(diff):
            mean_value = calculate_mean_criterion_value(product_data, competitor_data, category_criteria[k])
            score_diff[k] = mean_value
    return score_diff

# Main function to calculate the SD comparison matrix
def calculate_sd_comparison_matrix(product_data, competitor_data, category_criteria):
    """
    Calculate a 6x6 SD Comparison Matrix for a specific category, replacing NaN differences with the mean of the criteria.
    """
    # If there are no criteria, return a DataFrame of zeros
    if not category_criteria:
        return pd.DataFrame(
            np.zeros((6, 6)),
            index=[f"Product_{i+1}" for i in range(6)],
            columns=[f"Competitor_{j+1}" for j in range(6)]
        )
    
    sd_matrix = np.zeros((6, 6))  # Initialize a 6x6 matrix for SD values

    for i in range(6):  # Loop over product posts
        for j in range(6):  # Loop over competitor posts
            product_scores = product_data.iloc[i][category_criteria].values
            competitor_scores = competitor_data.iloc[j][category_criteria].values

            # Calculate score differences
            score_diff = calculate_score_differences(
                product_scores, competitor_scores, product_data, competitor_data, category_criteria
            )

            # Safely calculate the standard deviation
            if len(score_diff) > 0:
                sd_matrix[i, j] = np.std(score_diff)
            else:
                sd_matrix[i, j] = 0

    # Convert to DataFrame for better readability
    return pd.DataFrame(sd_matrix,
                        index=[f"Product_{i+1}" for i in range(6)],
                        columns=[f"Competitor_{j+1}" for j in range(6)])


# Calculate SD matrices for each category
branding_sd_matrix = calculate_sd_comparison_matrix(product_data, competitor_data, branding_criteria_filtered)
content_marketing_sd_matrix = calculate_sd_comparison_matrix(product_data, competitor_data, content_marketing_criteria_filtered)
social_media_marketing_sd_matrix = calculate_sd_comparison_matrix(product_data, competitor_data, social_media_marketing_criteria_filtered)

# Function to find the top SD values ensuring non-repetitive product and competitor image pairs
def find_top_non_repetitive_sd(sd_matrix, product_data, competitor_data, category, top_count=3):
    """
    Find the top SD values ensuring non-repetitive product and competitor image pairs within the same category.

    Args:
        sd_matrix: DataFrame representing the SD matrix.
        product_data: DataFrame containing product data (to extract image names).
        competitor_data: DataFrame containing competitor data (to extract image names).
        category: String representing the category name.
        top_count: Number of top results to return (default is 3).

    Returns:
        List of tuples containing category, product image name, competitor image name, and SD value.
    """
    used_product_images = set()
    used_competitor_images = set()
    top_results = []

    for i in range(sd_matrix.shape[0]):
        for j in range(sd_matrix.shape[1]):
            if len(top_results) == top_count:
                break

            product_image = product_data.iloc[i]['Image']
            competitor_image = competitor_data.iloc[j]['Image']
            sd_value = sd_matrix.iloc[i, j]

            if product_image not in used_product_images and competitor_image not in used_competitor_images:
                top_results.append((category, product_image, competitor_image, sd_value))
                used_product_images.add(product_image)
                used_competitor_images.add(competitor_image)

    return top_results

# Find top non-repetitive SD results
branding_top_3 = find_top_non_repetitive_sd(branding_sd_matrix, product_data, competitor_data, "Brand Marketing")
content_marketing_top_3 = find_top_non_repetitive_sd(content_marketing_sd_matrix, product_data, competitor_data, "Content Marketing")
social_media_marketing_top_3 = find_top_non_repetitive_sd(social_media_marketing_sd_matrix, product_data, competitor_data, "Social Media Marketing")

# Combine results into a DataFrame
all_top_3 = branding_top_3 + content_marketing_top_3 + social_media_marketing_top_3
top_3_df = pd.DataFrame(
    all_top_3,
    columns=['Category', 'Product_Image_Name', 'Competitor_Image_Name', 'SD_Value']
)

# Save results to Excel
top_3_df.to_excel("Output File/excel/top_3_sd_results.xlsx", index=False)

# Print the results
print("\nTop 3 SD Results DataFrame:")
print(top_3_df)
import os

output_folder = "data/output_generated_file/Output File/excel"
output_file_path = os.path.join(output_folder, "top_3_sd_results.xlsx")
os.makedirs(output_folder, exist_ok=True)
# Save results to the specified folder
top_3_df.to_excel(output_file_path, index=False)

# Print confirmation
print(f"Top 3 SD Results saved in: {output_file_path}")
