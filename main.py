import logging
import time
from voice_recognition import VoiceRecognition
from text_to_speech import TextToSpeech
from ai_agent import AIAgent

#Configurar logging
logging.basicConfig( 
    level = logging.WARNING, # Nivel de logging
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato del mensaje de logging
)

class LycaonAssistant:
    def __init__(self):
        print("Inicializando Lycaon ...") # Mensaje de inicio

        #Inicializar componentes
        self.voice_recognition = VoiceRecognition()
        self.tts = TextToSpeech()
        self.ai_agent = AIAgent()   

        #Configuración
        self.wake_word = "Lycaon" # Palabra de activación
        self.conversation_timeout = 30 # Tiempo de espera para la conversación en segundos
        self.conversation_mode = False # Modo conversación desactivado inicialmente
        self.last_interaction = None # Última interacción para manejar el tiempo de espera

        print("Lycaon inicializado y listo para escuchar.") # Mensaje de finalización de inicialización
        self.tts.speak("Hola, soy Lycaon, tu asistente personal. ¿En qué puedo ayudarte hoy?") # Mensaje de bienvenida

    def run(self):
        """Bucle principal del asistente"""

        try:

            while True:
                if not self.conversation_mode:
                    self._listen_for_wake_word() # Escuchar la palabra de activación
                else:
                    self._handle_conversation()
                

        except KeyboardInterrupt:
            print("\nApagando Lycaon.") # Mensaje de parada
            self.tts.speak("Adiós, que tengas un buen día.")
        except Exception as e:
            logging.error(f"Error Crítico: {e}")
            
    
    def _listen_for_wake_word(self):
        """Espera la palabra de activación para iniciar la conversación"""
        
        print("Escuchando la palabra de activación...")

        success, result = self.voice_recognition.listen_for_wake_word(
            self.wake_word, timeout= 10) # Escucha la palabra de activación con un timeout de 10 segundos

        if success: 
            logging.info(f"¡Activado! Escuché: {result}") # Log de detección de palabra de activación
            self.tts.speak("¿En qué puedo ayudarte?")
            self.conversation_mode = True # Cambia al modo conversación
            self.last_interaction = time.time() # Actualiza el tiempo de la última interacción
        
        elif "Timeout" not in result and "No se pudo" not in result:
            print(f" No activado: '{result}'")


    def _handle_conversation(self):
        """Maneja la conversación activa"""
        success, command = self.voice_recognition.listen_for_command(timeout=8)
        
        if success:
            print(f" Comando: '{command}'")
            
            # Comando especial para salir
            if any(word in command.lower() for word in ["adiós", "chao", "salir", "terminar"]):
                self.tts.speak("Hasta luego")
                self.conversation_mode = False
                return
            
            # Procesar comando con IA
            print(" Procesando...")
            response = self.ai_agent.process_command(command)
            
            print(f" Lycaon: {response}")
            self.tts.speak(response)
            
            self.last_interaction = time.time()
        else:
            print(f"❌ {command}")
            
            # Verificar timeout
            if (time.time() - self.last_interaction) > self.conversation_timeout:
                print(" Timeout - Regresando a modo espera")
                self.conversation_mode = False

if __name__ == "__main__":
    assistant = LycaonAssistant()
    assistant.run()
