import streamlit as st
import speech_recognition as sr
import pyttsx3
import nltk
from nltk.corpus import wordnet
import threading  

nltk.download('wordnet')
nltk.download('omw-1.4')

def speak(text):
    
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
    threading.Thread(target=run, daemon=True).start()  # Run in a background thread

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak now.")
        speak("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            st.error("Bot: Sorry, I couldn't understand. Please try again.")
            speak("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            st.error("Bot: Unable to connect to the voice recognition service.")
            speak("Unable to connect to the voice recognition service.")
            return None

st.title("🎙️ Dictionary Bot with Voice and Text")

mode = st.radio("Choose Mode:", ["Chat Mode", "Voice Mode"])
word = ""
if mode == "Chat Mode":
    word = st.text_input("Enter a word:")
elif mode == "Voice Mode":
    if st.button("🎤 Speak Now"):
        word = get_voice_input()
        if word:
            st.success(f"You said: {word}")

if word:
    if word.lower() == "exit":
        st.success("Bot: Goodbye!")
        speak("Goodbye!")
    else:
        synsets = wordnet.synsets(word)
        if synsets:
            meaning = synsets[0].definition()
            st.write(f"**Meaning of '{word}':**")
            st.info(meaning)
            speak(f"The meaning of {word} is {meaning}")

            synonyms = set()
            for synset in synsets:
                for lemma in synset.lemmas():
                    synonyms.add(lemma.name())

            if synonyms:
                st.write(f"**Synonyms of '{word}':**")
                st.success(", ".join(synonyms))  
        else:
            st.error("Bot: Sorry, I couldn't find the meaning.")
            speak("Sorry, I couldn't find the meaning.")