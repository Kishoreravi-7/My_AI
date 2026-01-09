import pyttsx3

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        
        female_voice = None
        for v in voices:
            if "female" in v.name.lower() or "zira" in v.name.lower():
                female_voice = v.id
                break
        if female_voice:
            self.engine.setProperty('voice', female_voice)
        else:
            self.engine.setProperty('voice', voices[0].id)
        
        self.engine.setProperty('rate', 150)    
        self.engine.setProperty('volume', 1.0)  

    def speak(self, text: str):
        if not text:
            return
        
        print(f"\n🔊 Lisa: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
