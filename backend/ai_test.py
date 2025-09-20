from google import genai
from decouple import config


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
GEMINI_API_KEY = config('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)