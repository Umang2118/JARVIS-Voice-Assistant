

from google import genai

from config import GEMINI_API_KEY

def aiProcess(command):
    """
    Processes a command using the Google Gemini API.
    """
    if GEMINI_API_KEY == "Gemini_api" or not GEMINI_API_KEY:
        return "I cannot connect to the AI service because the Gemini API key is missing or not configured."
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        system_instruction = "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=command,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, I am having trouble connecting to my brain right now."