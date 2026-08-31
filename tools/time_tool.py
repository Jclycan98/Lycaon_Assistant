from langchain.tools import tool
from datetime import datetime
import pytz

@tool

def get_time(city: str = "local") -> str:
    """Obtiene la hora actual en una ciudad especifica"""
    try:
        #Diccionario de ciudades y zonas horarias

        city_zones = {
            "bogota": "America/Bogota",
            "madrid": "Europe/Madrid",
            "new_york": "America/New_York",
            "london": "Europe/London",
            "tokyo": "Asia/Tokyo",
            "mexico_city": "America/Mexico_City",
            "local": "America/Bogota"  # Por defecto a Bogotá
        }

        city_key = city.lower()
        if city_key not in city_zones:
            return f"No reconozco la zona horaria de {city}"
        
        timezone = pytz.timezone(city_zones[city_key])
        current_time = datetime.now(timezone).strftime("%H:%M")
        current_date = datetime.now(timezone).strftime("%d de %B de %Y")

        return f"En {city.title()}: {current_time} del {current_date}"
    except Exception as e:
        return f"Error al obtener la hora: {e}"