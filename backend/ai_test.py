import google.generativeai as genai
from decouple import config


def main():
    """A simple script to test the Gemini API connection."""
    try:
        # Configure the API key from the environment variable `GEMINI_API_KEY`.
        api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=api_key)

        # Create the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Explain how AI works in a few words")
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()