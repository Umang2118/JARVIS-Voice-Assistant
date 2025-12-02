import pyttsx3
from gtts import gTTS
import pygame
import os
import time

engine = pyttsx3.init() 

def speak_old(text):
    """
    Classic TTS using pyttsx3 (might sound less natural but is fast and offline).
    """
    print(f"SPEAK_OLD: {text}")
    engine.say(text)
    engine.runAndWait()

def speak(text):
    """
    Modern TTS using gTTS and pygame (more natural voice, requires internet).
    """
    print(f"SPEAK: {text}")
    temp_file = 'temp.mp3'
    try:
    
        tts = gTTS(text, lang='en')
        tts.save(temp_file) 

        
        if not pygame.mixer.get_init():
             pygame.mixer.init()

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

    
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Error in speak function: {e}. Falling back to text output.")
        
        print(f"Assistant failed to speak: {text}")
    finally:
    
        if os.path.exists(temp_file):
            os.remove(temp_file)