# command_handler.py

import webbrowser
import os
from AppOpener import open as open_app

# Local Imports
from speech_utils import speak
from ai_core import aiProcess
from utility_funcs import get_current_time, get_weather, get_news_headlines, \
                           play_song_fast, play_song_fallback, \
                           take_screenshot, take_screenshot_async, \
                           shutdown_pc, restart_pc, lock_pc
from config import SYS_APPS, INSTALLED_APPS
from pathlib import Path
import speech_recognition as sr

recognizer = sr.Recognizer()
# Set recognizer properties for confirmation listening
recognizer.pause_threshold = 0.5 
recognizer.energy_threshold = 300 
recognizer.dynamic_energy_threshold = True 


def listen_for_confirmation():
    """Listens for a simple 'yes' or 'no' response."""
    print("Listening for Confirmation (Yes/No)...")
    try:
        with sr.Microphone() as source:
            # Listen for a very short phrase (3 seconds max)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        
        confirmation_word = recognizer.recognize_google(audio).lower().strip()
        print(f"Confirmation recognized: {confirmation_word}")
        
        if confirmation_word in ("yes", "yep", "confirm", "yeah", "ok"):
            return True
        elif confirmation_word in ("no", "nope", "cancel", "stop", "never"):
            return False
        else:
            return None # Neutral or unrecognized
            
    except sr.WaitTimeoutError:
        print("Confirmation timeout.")
        return None
    except sr.UnknownValueError:
        print("Could not understand confirmation audio.")
        return None
    except Exception as e:
        print(f"Error during confirmation listening: {e}")
        return None

def processCommand(c):
    """
    Main function to parse the user command and execute the corresponding action.
    """
    c_lower = c.lower().strip()
    
    # --- Web Browsing ---
    if c_lower.startswith("open google"):
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif c_lower.startswith("open facebook"):
        speak("Opening Facebook.")
        webbrowser.open("https://facebook.com")
    elif c_lower.startswith("open youtube"):
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    
    # --- App Launching (Custom Dictionary Check) ---
    elif c_lower.startswith("open"): 
        app_name = c_lower.replace("open", "", 1).strip()
        
        if app_name in SYS_APPS:
            speak(f"Opening {app_name}...")
            os.system(f"start {SYS_APPS[app_name]}") 
        
        elif app_name in INSTALLED_APPS:
            speak(f"Opening {app_name}...")
            try:    
                os.startfile(INSTALLED_APPS[app_name])
            except FileNotFoundError:
                speak(f"I could not find the path for {app_name}. Please update the path in config.py.")
        
        else:
            speak(f"I don't have {app_name} in my custom app database. Trying automated launch.")
            try:
                open_app(app_name, match_closest=True)
            except:
                speak(f"Sorry, I couldn't find or launch {app_name} automatically either.")

    # --- App Launching (AppOpener Library) ---
    elif c_lower.startswith("launch"):
        app_name = c_lower.replace("launch", "", 1).strip()
        speak(f"Launching {app_name}")
        try:
            open_app(app_name, match_closest=True)
        except:
            speak(f"Sorry, I couldn't find or launch {app_name}.")
            
    # --- Play Music/Video ---
    elif c_lower.startswith("play "):
        song_name = c_lower.replace("play ", "", 1).strip()
        if song_name:
            speak(f"Searching for {song_name} on YouTube.")
            url = play_song_fast(song_name, open_in_browser=True)
            
            if not url:
                speak("Primary search failed, trying fallback method.")
                play_song_fallback(song_name)
        else:
            speak("Please tell me the name of the song you want to play.")
            
    # --- Screenshot ---
    elif any(kw in c_lower for kw in ("take screenshot", "take a screenshot", "capture screen")):
        speak("Capturing screenshot now.")
        path = take_screenshot(open_after=False)
        if path:
            speak(f"Screenshot saved as {Path(path).name}.")
            print("Screenshot saved at:", path)
        else:
            speak("Sorry, I couldn't take the screenshot.")
            
    # --- News ---
    elif "news" in c_lower:
        get_news_headlines()
            
    # --- Time/Date ---
    elif "time" in c_lower or "date" in c_lower:
        response = get_current_time()
        speak(response)
        
    # --- Weather ---
    elif "weather" in c_lower:
        response = get_weather(c) 
        speak(response)
    
    # --- Power Management ---
    
    elif "shutdown" in c_lower or "shut down" in c_lower:
        speak("Are you sure you want to shut down the computer? Please say 'yes' or 'no'.")
        
        if listen_for_confirmation():
            response = shutdown_pc(delay_seconds=5) # 5-second safety delay
            speak(response)
        else:
            speak("Shutdown cancelled.")
            
    elif "restart" in c_lower:
        speak("Are you sure you want to restart the computer? Please say 'yes' or 'no'.")
        
        if listen_for_confirmation():
            response = restart_pc(delay_seconds=5) # 5-second safety delay
            speak(response)
        else:
            speak("Restart cancelled.")

    elif "lock" in c_lower or "lock the pc" in c_lower:
        response = lock_pc()    
        speak(response)

        output = aiProcess(c)
        speak(output)