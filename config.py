

from pathlib import Path

NEWSAPI_KEY = "YOUR_API_KEY" 
OPENWEATHERMAP_KEY = "YOUR_API_KEY"
GEMINI_API_KEY = "YOUR_API_KEY" # (Replaced original key with placeholder)


SYS_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "explorer": "explorer.exe",
    "file manager": "explorer.exe",  
    "settings": "ms-settings:",     
    "photos": "ms-photos:",        
}


INSTALLED_APPS = {
    "vs code": r"C:\Users\Pc\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
    "chrome": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
    "whatsapp": r"C:\Users\YourUser\AppData\Local\WhatsApp\WhatsApp.exe", 
    "adobe": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Adobe Acrobat.lnk", 
    
}


SCREENSHOT_DIR = Path.cwd() / "screenshots"
DEFAULT_WEATHER_CITY = "Lucknow"