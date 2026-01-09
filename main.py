import sys
import os
from lisa.ai_engine import LisaAI
from lisa.speech_recognition_module import VoiceInput
from lisa.text_to_speech import VoiceOutput


def print_header():
    print("\n" + "=" * 60)
    print("  LISA - Your Intelligent Voice AI Assistant")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type 'voice' or 'v' to use voice input")
    print("  - Type 'clear' to reset conversation")
    print("  - Type 'quit' or 'exit' to leave")
    print("  - Or just type your message directly")
    print("-" * 60)


def check_api_key():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\nError: GROQ_API_KEY not found in environment variables.")
        print("Please set your Groq API key to use Lisa.")
        return False
    return True


def main():
    if not check_api_key():
        sys.exit(1)
    
    print_header()
    
    lisa = LisaAI()
    voice_input = VoiceInput()
    voice_output = VoiceOutput()
    
    mic_available = voice_input.check_microphone()
    if mic_available:
        print("[OK] Microphone detected - voice input available")
    else:
        print("[!] No microphone detected - using text input only")
    
    print("\nLisa: Hello! I'm Lisa, your AI assistant. How can I help you today?\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\nLisa: Goodbye! It was nice talking with you. Take care!")
                break
            
            if user_input.lower() == 'clear':
                message = lisa.clear_context()
                print(f"\n{message}")
                continue
            
            if user_input.lower() in ['voice', 'v']:
                if not mic_available:
                    print("Microphone not available. Please type your message instead.")
                    continue
                
                spoken_text = voice_input.listen()
                if spoken_text:
                    print(f"You said: {spoken_text}")
                    user_input = spoken_text
                else:
                    print("Could not understand. Please try again or type your message.")
                    continue
            
            print("\nLisa is thinking...")
            response = lisa.process_command(user_input)
            
            voice_output.speak(response)
            
        except KeyboardInterrupt:
            print("\n\nLisa: Goodbye! Take care!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
