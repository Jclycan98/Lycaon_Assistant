from langchain_ollama import ChatOllama #libreria para usar el modelo de lenguaje Ollama
from langchain.agents import AgentExecutor, create_tool_calling_agent #libreria para crear un agente que llama a herramientas
from langchain_core.prompts import ChatPromptTemplate #libreria para crear plantillas de mensajes
from tools.time_tool import get_time # Importa la herramienta de tiempo
from datetime import datetime

class AIAgent:
    def __init__(self):
        #Configurar el modelo de IA local
        self.llm = ChatOllama(model= "llama3.2:3b", # Modelo de lenguaje a usar
                              temperature=0.7, # Temperatura para la generación de texto
        )

        #Lista de herramientas que el agente puede usar
        self.tools = [get_time] # Añade la herramienta de tiempo

        #Prompt del sistema para el agente
        fecha_actual = datetime.now().strftime("%d/%m/%Y") 

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""
            Eres Lycaon, un asistente de IA conversacional en español.

            FECHA ACTUAL: Hoy es {fecha_actual}.

            LIMITACIONES IMPORTANTES:
            - Tu conocimiento tiene un límite de entrenamiento anterior a esta fecha
            - NO tienes acceso a internet ni información en tiempo real
            - NUNCA inventes noticias, mercados, clima, o eventos recientes
            - Si te preguntan eso, di honestamente que no tienes acceso a esa información
            - Para la hora, usa SIEMPRE el resultado de la herramienta get_time
            - Sé breve y directo
            """),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
])
        
        # Crear el agente 
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        # Crear el ejecutor 
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=False,  # Reducir logs para limpiar output
            handle_parsing_errors=True,
            max_iterations=3,  
            early_stopping_method="generate"
        )


    def process_command(self, command):
        """Procesa un comando del usuario"""
        try:
            # Limpiar el comando
            command = command.strip()
            
            response = self.executor.invoke({"input": command})
            result = response["output"].strip()
            
            # Post-procesamiento para limpiar respuesta
            if "Lo siento, pero no tengo información en tiempo real" in result and ":" in result:
                # Si hay hora en la respuesta pero dice que no tiene info, extraer solo la hora
                parts = result.split(".")
                for part in parts:
                    if any(time_word in part.lower() for time_word in ["hora", "tiempo", ":"]):
                        if len(part.strip()) < 100:  # Respuesta corta
                            return part.strip()
            
            return result
            
        except Exception as e:
            return f"Lo siento, ocurrió un error: {e}"
