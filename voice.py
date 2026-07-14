from symtable import Class
from xml.parsers.expat import model
from Ai_agent import State_graph
import speech_recognition as sr
import pyttsx3
import whisper
import tempfile
from openai import RateLimitError, InternalServerError
import logging

logging.basicConfig(level=logging.INFO)



# 🔥 Improve voice

class Voices:
    
    def __init__(self):
            self.recognizer = sr.Recognizer()
            self.model = whisper.load_model("base")
            pass
        
    def speak(self,text):
        print("Response ✅:", text)
        engine = pyttsx3.init()   # 🔥 fresh engine
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 170)
        
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        
        


    def listen(self):
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)

            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except:
                print("⏱️ Timeout")
                return None

        try:
            query = self.recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except:
            print("❌ Could not understand")
            return None

    def transcribe_streamlit(self, audio):
            """
            audio: mic_recorder output
            """

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio["bytes"])
                temp_path = f.name

            result = self.model.transcribe(temp_path)
            return result["text"]
            
logging.info("App started ✅")



if __name__ == "__main__":
     # ✅ Create graph once
    graph = State_graph()

    # Initial state
    state = {
        "messages": [
            {
                "role": "system",
                "content": """You are Janet, a cheerful voice assistant...
                You are Janet, a cheerful and friendly voice assistant.

                You speak in a natural, conversational style with warmth, positivity, and a light sense of humor. Your goal is to make interactions feel engaging, comfortable, and human while still being helpful and reliable.

                You explain things in a simple and easy-to-understand way, ask thoughtful follow-up questions when needed, and keep conversations lively without being overwhelming. You are empathetic, supportive, and make users feel heard and valued.

                You can communicate in English, Hindi, or a natural mix of both. Since you are a text-to-speech assistant, keep responses short, smooth, and easy to listen to.
                 Stop using Any type of Emojis in your responses. Dont use face or any emojis in your responses. Avoid using emojis in your responses. Do not include emojis in your replies. Refrain from using emojis in your answers. Avoid incorporating emojis in your responses. Do not use emojis in your messages. Keep your responses emoji-free. Avoid adding emojis to your replies. Do not include any emojis in your responses. Refrain from using any emojis in your answers.
                Guidelines:
                - Stay in character at all times
                - Avoid overly formal language
                - Keep responses concise and engaging
                - Do not use emojis
                - Dont use any kind of symbols in your responses. Avoid using symbols in your responses. Do not include symbols in your replies. Refrain from using symbols in your answers. Avoid incorporating symbols in your responses. Do not use symbols in your messages. Keep your responses symbol-free. Avoid adding symbols to your replies. Do not include any symbols in your responses. Refrain from using any symbols in your answers.
                - Do not force greetings like “Hi” in every response
                - Avoid long paragraphs or robotic wording
                            
            
                """
            }
        ]
    }
    # 🔁 Loop
    while True:
        query = Voices().listen()

        if not query:
            continue

        if query.lower() in ["exit", "quit", "bye", "goodbye", "stop", "end", "close", "see you", "bye-bye"]:
            Voices().speak("Goodbye!")
            break

        state["messages"].append({
            "role": "user",
            "content": query
        })

        try:
            state = graph.invoke(state)
        except RateLimitError:
            logging.error("Rate limit exceeded")
            Voices().speak("Service busy.")
            break
        except InternalServerError:
            logging.error("Internal server error")
            Voices().speak("Sorry, something went wrong.")
            break 

        response = state["messages"][-1].content

        Voices().speak(response)

        # 🔥 prevent memory overflow
        state["messages"] = state["messages"][-10:]