# pip install fastapi uvicorn requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

# pip install deep_translator
# pip install SpeechRecognition
import speech_recognition as sr
from deep_translator import GoogleTranslator
from io import BytesIO

def recognize_speech_from_audio_file(audio_data, language):
    """Recognize speech from an audio file and convert it to text."""
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(BytesIO(audio_data)) as source:
            audio = recognizer.record(source)  # Read the entire audio file

            # print("Recognizing...")
            text = recognizer.recognize_google(audio, language=language)
            # print(f"Recognized Text: {text}")
            return text
    except sr.UnknownValueError:
        return {"error":"Sorry, I could not understand the audio."}
    except sr.RequestError:
        return {"error":"Could not request results from Google Speech Recognition service."}


def translate_textDP(text, src_language, dest_language="en"):
    translator = GoogleTranslator(source=src_language, target=dest_language)
    translation = translator.translate(text)
    # print(f"Translated Text: {translation}")
    return translation


app = FastAPI()

@app.post('/recognize-and-translate/')
async def recognize_and_translate(
        file: UploadFile = File(...),
        language: str = Form(...)
):
    language_codes_STT = {
        "Arabic": "ar-SA",
        "Urdu": "ur-PK",
        "Chinese": "zh-CN",
        "Filipino (Tagalog)": "fil-PH",
        "Bengali": "bn-IN",
        "Spanish": "es-ES",
        "German": "de-DE",
        "French": "fr-FR",
        "Farsi": "fa-IR"
    }
    language_codes_TTS = {
        "Arabic": "ar",
        "Urdu": "ur",
        "Chinese": "zh",
        "Filipino (Tagalog)": "tl",
        "Bengali": "bn",
        "Spanish": "es",
        "German": "de",
        "French": "fr",
        "Farsi": "fa"
    }

    if language not in language_codes_STT or language not in language_codes_TTS:
        raise HTTPException(status_code=400, detail={"error":"Unsupported language"})

    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail={"error":"Invalid file type. Only WAV files are accepted."})

    try:
        # Read the audio data from the uploaded file
        audio_data = await file.read()

        # Recognize speech from the audio file
        recognized_text = recognize_speech_from_audio_file(audio_data, language_codes_STT[language])
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error":"Could not read file and recognize the text"})

    if recognized_text.startswith("Sorry") or recognized_text.startswith("Could not"):
        raise HTTPException(status_code=500, detail={"error":recognized_text})

    translated_text = translate_textDP(recognized_text, language_codes_TTS[language], "en")
    # print("Translated Text", translated_text)

    response_object = {
        "translated_text": str(translated_text),
        "language_text": str(recognized_text)
    }
    return response_object