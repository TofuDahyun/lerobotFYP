import speech_recognition as sr
import socket
import sys

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Checks if there is an active internet connection by trying to 
    connect to a public DNS server (Google DNS).
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def get_user_input(question):
    """
    Logic:
    1. Check Internet.
    2. Wait 3s for speech to START (timeout).
    3. If speech starts, listen indefinitely.
    4. If speech STOPS, wait 3s for more speech (pause_threshold).
    5. If silence persists for 3s after speech, process text.
    6. Fallback to text input on errors.
    """
    
    # 1. Check Internet Connection First
    if not check_internet_connection():
        print("\n[!] No internet connection detected.")
        print("    Skipping voice recognition. Please type your response.\n")
        return input(f"{question} (Text): ")

    # 2. Initialize Recognizer
    recognizer = sr.Recognizer()
    
    # CONFIGURATION FOR TIMING
    # Wait 3 seconds of silence AFTER speaking stops before finalizing the phrase
    recognizer.pause_threshold = 3.0 
    
    try:
        with sr.Microphone() as source:
            print(f"\n{question}")
            print("    🎤 Listening... (3s to start, 3s silence to end)")
            
            # Adjust for ambient noise quickly
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
            # 3. Listen with specific timeouts
            # timeout=3: Max time to wait for speech to START
            # phrase_time_limit=None: No max limit on how long you can talk
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=None)
            
            print("    Processing voice...")
            
            # Convert speech to text using Google
            text = recognizer.recognize_google(audio)
            print(f"    ✅ Voice detected: '{text}'")
            return text

    except sr.WaitTimeoutError:
        # 4. Fallback: Triggered if 3 seconds pass at the START with no speech
        print("\n    ⏱️  No speech started within 3 seconds.")
        return input(f"{question} (Text): ")
        
    except sr.UnknownValueError:
        print("\n    ❌ Could not understand audio.")
        return input(f"{question} (Text): ")
        
    except sr.RequestError:
        print("\n    ❌ Voice API request failed.")
        return input(f"{question} (Text): ")
        
    except OSError:
        print("\n    ❌ Microphone not accessible.")
        return input(f"{question} (Text): ")

# --- Main System Integration Example ---
if __name__ == "__main__":
    print("--- SYSTEM STARTED ---")
    
    # Example Question
    q1 = "Please describe your issue in detail."
    response = get_user_input(q1)
    
    print(f"\nSYSTEM RECEIVED: {response}\n")
    print("--- SYSTEM FINISHED ---")