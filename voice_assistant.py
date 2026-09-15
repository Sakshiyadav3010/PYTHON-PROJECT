"""
Voice Assistant (Beginner Tier)
---------------------------------
A simple voice assistant that:
    - Listens to spoken commands via a microphone (speech_recognition)
    - Responds using text-to-speech (pyttsx3)
    - Greets the user, tells the time/date, performs web searches,
      and asks the user to repeat itself if it doesn't understand

Setup:
    pip install SpeechRecognition pyttsx3 pyaudio

    Note: pyaudio can be tricky to install on some systems.
        Windows : pip install pyaudio
        macOS   : brew install portaudio && pip install pyaudio
        Linux   : sudo apt-get install python3-pyaudio

Text-mode fallback:
    If speech_recognition/pyttsx3/a microphone aren't available (e.g. this
    is being tested on a server with no audio hardware), the assistant
    automatically falls back to typed input and printed responses, so the
    exact same command logic can still be exercised and tested.

Run:
    python voice_assistant.py
"""

import datetime
import webbrowser
import sys

# ---------------------------------------------------------------------------
# Try to load voice libraries. If they (or a microphone) aren't available,
# fall back to a text-based interface using the same command logic below.
# ---------------------------------------------------------------------------
VOICE_MODE = True
try:
    import speech_recognition as sr
    import pyttsx3

    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()

    # Quick check that a microphone actually exists; if not, fall back.
    if sr.Microphone.list_microphone_names() == []:
        VOICE_MODE = False
except Exception:
    VOICE_MODE = False


def speak(text: str) -> None:
    """Output a response, either aloud (voice mode) or printed (text mode)."""
    print(f"Assistant: {text}")
    if VOICE_MODE:
        tts_engine.say(text)
        tts_engine.runAndWait()


def listen() -> str:
    """Capture one command, either from the microphone or the keyboard."""
    if VOICE_MODE:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is unavailable right now.")
            return ""
    else:
        try:
            command = input("You (type your command): ")
        except EOFError:
            return "exit"
        return command.lower()


def handle_command(command: str) -> bool:
    """
    Process a single command.
    Returns False if the assistant should stop running, True otherwise.
    """
    if not command:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return True

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")

    elif "search" in command:
        # Extract the search topic after the word "search"
        topic = command.split("search", 1)[1].strip()
        topic = topic.replace("for", "", 1).strip() if topic.startswith("for") else topic
        if not topic:
            speak("What would you like me to search for?")
            topic = listen()
        if topic:
            speak(f"Searching the web for {topic}.")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        else:
            speak("Sorry, I didn't get a search topic.")

    elif "exit" in command or "quit" in command or "stop" in command or "goodbye" in command:
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("I'm not sure how to help with that yet. "
              "Try saying 'hello', 'what's the time', 'what's the date', "
              "'search for ...', or 'exit'.")

    return True


def main():
    mode_label = "voice" if VOICE_MODE else "text (no microphone detected)"
    print("=" * 50)
    print("            PYTHON VOICE ASSISTANT")
    print(f"            Mode: {mode_label}")
    print("=" * 50)
    speak("Hi, I'm your assistant. Say 'hello', ask for the time or date, "
          "ask me to search something, or say 'exit' to quit.")

    running = True
    while running:
        command = listen()
        running = handle_command(command)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant stopped.")
        sys.exit(0)
