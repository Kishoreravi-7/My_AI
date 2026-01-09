import speech_recognition as sr


class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
    
    def listen(self) -> str:
        try:
            with sr.Microphone() as source:
                print("\nListening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
                print("🔄 Processing speech...")
                
                text = self.recognizer.recognize_google(audio)
                return text
                
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            return ""
        except Exception as e:
            print(f"❌ Error capturing audio: {e}")
            return ""
    
    def check_microphone(self) -> bool:
        try:
            with sr.Microphone() as source:
                return True
        except Exception:
            return False
