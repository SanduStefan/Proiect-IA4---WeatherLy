from city_manager import DESTINATIONS, TOP_CITIES
from weather_data import get_weather
from utils import weather_message

def get_chatbot_response(user_input):
    user_input = user_input.lower()
    
    # 1. Verificare daca utilizatorul intreaba de un oras specific
    for city in TOP_CITIES:
        if city.lower() in user_input:
            data = get_weather(city)
            if "error" not in data:
                advice = weather_message(data["temperature"], data["condition"])
                return f"În {city} sunt {data['temperature']}°C ({data['condition']}). Sfat haine: {advice}"
            return f"Știu unde e {city}, dar am probleme cu senzorii meteo acum."

    # 2. Logica de recomandari bazata pe preferinte
    results = DESTINATIONS
    if any(word in user_input for word in ["recomand", "vreau", "caut", "unde"]):
        if "cald" in user_input or "soare" in user_input:
            results = [d for d in results if d["type"] == "cald"]
        elif "rece" in user_input or "zapada" in user_input or "frig" in user_input:
            results = [d for d in results if d["type"] == "rece"]
        
        if "natura" in user_input or "plimbare" in user_input:
            results = [d for d in results if d["nature"] in ["munte", "jungla", "parcuri", "fiorduri"]]
            
        if "mic" in user_input or "ieftin" in user_input:
            results = [d for d in results if d["budget"] == "mic"]

        if results and len(results) < len(DESTINATIONS):
            names = [d["name"] for d in results[:3]]
            return f"Îți sugerez să mergi în: {', '.join(names)}. Despre care vrei să afli ce haine să îți iei?"
        
        return "Spune-mi dacă preferi ceva cald, rece, natură sau un buget anume!"

    # 3. FAQ de baza
    faq = {
        "salut": "Bună! Sunt asistentul tău WeatherLy. Îți pot recomanda destinații sau îți pot spune ce haine să porți într-un oraș!",
        "haine": "Dacă îmi spui orașul, îți fac imediat bagajul virtual!",
        "mersi": "Cu plăcere! Zbor lin și vreme însorită!"
    }
    for key, val in faq.items():
        if key in user_input: return val

    return "Interesant! Întreabă-mă despre un oraș anume sau cere-mi o recomandare (ex: 'recomanda-mi ceva cald')."