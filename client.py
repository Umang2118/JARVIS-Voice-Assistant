from google import genai 

# NOTE: Replace 'YOUR_GEMINI_API_KEY' with your actual key.
GEMINI_API_KEY = "YOUR_API_KEY"

client = genai.Client(api_key=GEMINI_API_KEY)


system_instruction = "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud."


response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="what is coding",
    config=genai.types.GenerateContentConfig(
        system_instruction=system_instruction
    )
)

print(response.text)