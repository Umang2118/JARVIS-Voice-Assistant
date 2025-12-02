

import speech_recognition as sr
import time


from speech_utils import speak 
from command_handler import processCommand 

recognizer = sr.Recognizer()

if __name__ == "__main__":
    
    recognizer.pause_threshold = 0.5
    recognizer.energy_threshold = 300 
    recognizer.dynamic_energy_threshold = True 
    
    speak("Initializing jarvis....")
    
   
    try:
        with sr.Microphone() as source:
            print("Calibrating background noise... Please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Calibration Complete.")
    except Exception as e:
        print(f"Microphone initialization or calibration failed: {e}")


    
    while True:
        print("\n--- Listening for Activation Word (Jarvis) ---")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3) 
            
            
            word = recognizer.recognize_google(audio)
            
            if(word.lower().strip() in ("jarvis", "ok jarvis")): 
                speak("Yes, how can I help?") 
                
                
                with sr.Microphone() as source:
                    print("jarvis Active... Speak Command")
                    recognizer.pause_threshold = 0.5 
                    audio = recognizer.listen(source, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")
 
                    processCommand(command)
                    
        except KeyboardInterrupt:
            print("Exiting Assistant.")
            break 
        except sr.WaitTimeoutError:
            pass 
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            time.sleep(1) 
            pass
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pass