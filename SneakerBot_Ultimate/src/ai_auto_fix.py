import openai
from utils.logger import log_error
from utils.helper_functions import extract_site_structure

openai.api_key = "YOUR_OPENAI_API_KEY"


def detect_website_changes(site_url):
    """Analyzes site structure changes and suggests fixes using AI."""
    try:
        site_code = extract_site_structure(site_url)
        prompt = f"Analyze this website structure and suggest fixes for automation:\n{site_code}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["choices"][0]["message"]["content"]
    except Exception as e:
        log_error(f"AI Auto-Fix Error: {e}")
        return "No fix suggestions available."