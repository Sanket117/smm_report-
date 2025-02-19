import subprocess
import sys

def install_requirements():
    """Ensure dependencies are installed before running scripts."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to install dependencies: {e}")

def run_python_file(file_name, company_name):
    """Run a Python script with subprocess."""
    try:
        result = subprocess.run(
            [sys.executable, file_name, company_name],  
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return "success", result.stdout  
        else:
            return "error", f"Error in {file_name}: {result.stderr}"
    except Exception as e:
        return "error", f"An error occurred while running {file_name}: {str(e)}"

def main():
    if len(sys.argv) > 1:
        company_name = sys.argv[1]
    else:
        company_name = "Default_Company"

    install_requirements()  # Install requirements before execution

    scripts = [
        'src/input_analysis/product-analysis/product_analysis.py',
        'src/input_analysis/competitor-analysis/competitor_analysis.py',
        'src/input_analysis/Standarddeviation.py',
        'src/input_analysis/renamebranding.py',
        'src/input_analysis/path.py',
        'src/input_analysis/feedback.py',
        'src/templates/brand.py',
        'src/templates/content.py',
        'src/templates/social.py',
        'src/Report/updated1.py',
        'src/Report/Report.py'
    ]

    for script in scripts:
        status, message = run_python_file(script, company_name)
        if status == "error":
            print(message)
            return
        else:
            print(f"{script} executed successfully.")

    # ✅ After all scripts run successfully, mark the status as "done"
    with open("src/Report/status.txt", "w") as f:
        f.write("done")

if __name__ == "__main__":
    main()
