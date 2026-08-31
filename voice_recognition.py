import speech_recognition as sr
import logging

class VoiceRecognition:
    def __init__(self, mic_index = 0):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index= mic_index)

        #Calibrar para ruido ambiente
        with self.mic as source:
            print("🎙️ Calibrando micrófono...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)

               # Configuración mejorada
        self.recognizer.energy_threshold = 3000  # Ajustar sensibilidad
        self.recognizer.dynamic_energy_threshold = True # Activar umbral dinámico
        self.recognizer.pause_threshold = 0.8  # Pausa más corta
        self.recognizer.phrase_threshold = 0.3 # Umbral de frase más bajo

    def listen_for_wake_word(self, wake_word = "Lycaon", timeout=5):
        """Escucha la palabra de activación."""
        try:
            with self.mic as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio, language="es-ES" or "en-US").lower()

                #Mejorar detección de variantes de "Lycaon"
                wake_variants= [wake_word.lower(), "licaón", "lican", "lycaon", "li caon", "limon", "limón"]


                if any(variant in text for variant in wake_variants):
                    return True, text
                return False, text
        
        except sr.WaitTimeoutError:
            return False, "Timeout esperando audio"
        except sr.UnknownValueError:
            return False, "No se pudo entender el audio"
        except sr.RequestError as e:
            return False, f"Error: {e}"
        
    def listen_for_command(self, timeout= 10):
        """Escucha un comando de voz del usuario."""
        try:
            with self.mic as source:
                print("🎙️ Hablando...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                # Intentar múltiples configuraciones
                for language in ['es-ES', 'es-MX', 'es', 'en-US']:
                    try:
                        command = self.recognizer.recognize_google(audio, language=language)
                        return True, command.strip() # Limpiar espacios
                    except:
                        continue
                
                return False, "No se pudo reconocer en ningún idioma"
        
        except sr.WaitTimeoutError:
            return False, "Timeout esperando comando"
        
        except sr.UnknownValueError:
            return False, "No se pudo entender el comando"
        
        except sr.RequestError as e:
            return False, f"Error: {e}"


        