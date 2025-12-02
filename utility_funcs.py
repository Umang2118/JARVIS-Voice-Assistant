import datetime
import threading
import os
import sys
import webbrowser
from pathlib import Path


from pyowm import OWM
import requests
import mss
import mss.tools
from PIL import Image 
import yt_dlp
import pywhatkit 
from speech_utils import speak
from config import OPENWEATHERMAP_KEY, NEWSAPI_KEY, DEFAULT_WEATHER_CITY, SCREENSHOT_DIR



# --- System Power Management Functions ---

def shutdown_pc(delay_seconds=1):
    """Shuts down the computer after a specified delay."""
    if sys.platform.startswith('win'):
        # Windows command: /s (shutdown), /t (time delay in seconds)
        os.system(f"shutdown /s /t {delay_seconds}")
        return "Shutting down the computer."
    elif sys.platform == 'darwin':
        # macOS command: 'now' can be replaced by a time string
        os.system("shutdown -h now") 
        return "Shutting down the computer."
    elif sys.platform.startswith('linux'):
        # Linux command: -h (halt)
        os.system("shutdown -h now")
        return "Shutting down the computer."
    else:
        return "Sorry, shutdown is not supported on this operating system."

def restart_pc(delay_seconds=1):
    """Restarts the computer after a specified delay."""
    if sys.platform.startswith('win'):
        # Windows command: /r (restart), /t (time delay in seconds)
        os.system(f"shutdown /r /t {delay_seconds}")
        return "Restarting the computer."
    elif sys.platform == 'darwin':
        os.system("shutdown -r now")
        return "Restarting the computer."
    elif sys.platform.startswith('linux'):
        os.system("shutdown -r now")
        return "Restarting the computer."
    else:
        return "Sorry, restart is not supported on this operating system."

def lock_pc():
    """Locks the computer screen."""
    if sys.platform.startswith('win'):
        # Windows command: Rundll32.exe for locking the workstation
        os.system("Rundll32.exe user32.dll,LockWorkStation")
        return "Locking the computer."
    elif sys.platform == 'darwin':
        # macOS command: Requires an external script or app to be run
        os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
        return "Locking the computer."
    elif sys.platform.startswith('linux'):
        # Linux command: Works with most common desktop environments (like gnome, kde)
        os.system("xdg-screensaver lock")
        return "Locking the computer."
    else:
        return "Sorry, locking the screen is not supported on this operating system."
    
    
# --- Time Functionality ---
def get_current_time():
    """Provides the current time and date."""
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    return f"The current time is {time_str} and today is {date_str}."

# --- Weather Functionality ---
def get_weather(city_command): 
    """Extracts the city name and fetches weather using OWM."""
    city = DEFAULT_WEATHER_CITY
    
    c_lower = city_command.lower()
    if "weather in" in c_lower:
        parts = c_lower.split("weather in")
        if len(parts) > 1 and parts[-1].strip():
            city = parts[-1].strip()

    if not OPENWEATHERMAP_KEY:
        return "The OpenWeatherMap API key is not configured. Please add your key to config.py."

    try:
        owm = OWM(OPENWEATHERMAP_KEY)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        weather = observation.weather

        temp_c = weather.temperature('celsius')['temp']
        status = weather.status.lower() 
        
        response = f"The weather in {city.title()} is currently {status}, with a temperature of {temp_c:.1f} degrees Celsius."
        
    except Exception as e:
        response = f"Sorry, I couldn't get the weather information for {city.title()}. Check the city name or the API key."
        print(f"Weather Error: {e}")
        
    return response

# --- News Functionality ---
def get_news_headlines():
    """Fetches and speaks the top news headlines for India using NewsAPI."""
    if not NEWSAPI_KEY:
        speak("The NewsAPI key is not configured. Please add your key to config.py.")
        return

    speak("Fetching the latest news headlines.")
    
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWSAPI_KEY}")
        r.raise_for_status() 
        
        data = r.json()
        articles = data.get('articles', [])
        
        if articles:
            for i, article in enumerate(articles[:3]):
                speak(f"Headline number {i+1}: {article.get('title', 'No title available')}")
        else:
            speak("Sorry, I could not retrieve any news at the moment.")
            
    except requests.exceptions.RequestException as e:
        speak("I encountered an error while trying to fetch the news. Check your internet connection or API key.")
        print(f"News API Error: {e}")

# --- YouTube/Song Playback ---
def play_song_fast(song_name, open_in_browser=True):
    """Uses yt-dlp to quickly get the top YouTube result URL and opens it."""
    if not song_name or not song_name.strip():
        return None

    query = f"ytsearch1:{song_name}"
    ydl_opts = {"skip_download": True, "quiet": True, "nocheckcertificate": True, "extract_flat": True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
            video = info.get("entries", [None])[0]
            if not video:
                return None

            vid_url = "https://www.youtube.com/watch?v=" + video.get("id")
            
            if vid_url and open_in_browser:
                webbrowser.open(vid_url)
            return vid_url
            
    except Exception as e:
        print("play_song_fast - yt-dlp error:", e)
        return None

def play_song_fallback(song_name):
    """Uses pywhatkit as a fallback for playing songs on YouTube."""
    try:
        pywhatkit.playonyt(song_name)
    except Exception as e:
        speak("Sorry, I couldn't play that song right now using the fallback method.")
        print("Fallback play error:", e)

# --- Screenshot Functionality ---
def take_screenshot(filename=None, region=None, open_after=False):
    """Fast screenshot using mss."""
    try:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        # Determine save path
        if not filename:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = SCREENSHOT_DIR / f"screenshot_{ts}.png"
        else:
            save_path = Path(filename) if Path(filename).is_absolute() else SCREENSHOT_DIR / Path(filename)
            
        with mss.mss() as sct:
            monitor = sct.monitors[0] # Full primary screen for simplicity
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(save_path))

        # Open image after save (for Windows/Mac/Linux)
        if open_after:
            if sys.platform.startswith('win'):
                os.startfile(str(save_path))
            else:
                os.system(f'open "{save_path}"' if sys.platform == 'darwin' else f'xdg-open "{save_path}"')

        return str(save_path)
    except Exception as e:
        print("take_screenshot error:", e)
        return None

def take_screenshot_async(*args, **kwargs):
    """Takes a screenshot in a separate thread to prevent blocking the main loop."""
    threading.Thread(target=take_screenshot, args=args, kwargs=kwargs, daemon=True).start()