import pyttsx3 # libreria de texto a voz
import logging # libreria para registrar eventos

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()

    def setup_voice(self):
        """Configura la voz del sistema"""
        voices = self.engine.getProperty('voices')

        #Buscar una voz masculina en español

        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break # Si no se encuentra una voz en español, se usará la predeterminada

        self.engine.setProperty('rate', 180)  # Velocidad de la voz, palabras por minuto
        self.engine.setProperty('volume', 1.0) # volumen maximo
    
    def speak(self, text: str):
        """Convierte texto a voz"""
        try:
            print(f"lycaon: {text}")  # Imprime el texto que se va a hablar
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Error al convertir en TTS: {e}")
            return f"Error al hablar: {e}"