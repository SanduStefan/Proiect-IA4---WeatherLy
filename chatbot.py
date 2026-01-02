import unicodedata
from city_manager import DESTINATIONS, TOP_CITIES
from weather_data import get_weather
from utils import weather_message

def remove_diacritics(text):
    if not text:
        return ""
    return "".join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

def get_chatbot_response(user_input, user_profile=None):
    raw_input = user_input.lower()
    clean_input = remove_diacritics(raw_input)
    interests = remove_diacritics(user_profile.get('interests', '').lower()) if user_profile else ""
    
    # --- 1. DETECȚIE ORAȘE ---
    found_cities = []
    # Sortăm TOP_CITIES după lungime (descrescător) pentru a evita suprapunerile (ex: "Satu Mare" vs "Mare")
    sorted_cities = sorted(TOP_CITIES, key=len, reverse=True)
    
    for city in sorted_cities:
        city_clean = remove_diacritics(city.lower())
        if city_clean in clean_input:
            found_cities.append(city)
            # Ștergem orașul găsit din input-ul temporar pentru a nu-l găsi de două ori
            clean_input = clean_input.replace(city_clean, "", 1)
    
    # --- 2. LOGICĂ COMPARARE (Declanșată dacă avem 2 orașe SAU cuvinte de comparație) ---
    if len(found_cities) >= 2 or (len(found_cities) == 2 and any(word in clean_input for word in ["compara", "fata de", "vs", "versus"])):
        c1, c2 = found_cities[0], found_cities[1]
        w1, w2 = get_weather(c1), get_weather(c2)
        
        if "error" not in w1 and "error" not in w2:
            t1, t2 = w1['temperature'], w2['temperature']
            diff = abs(t1 - t2)
            better = c1 if t1 > t2 else c2
            
            return (f"Analiză comparativă: În {c1} sunt {t1}°C, iar în {c2} sunt {t2}°C. "
                    f"Diferența este de {diff}°C. Dacă preferi căldura, {better} este alegerea mai bună!")

    # --- 3. ALERTE METEO EXTREME ---
    if any(word in clean_input for word in ["alerta", "pericol", "furtuna", "extrem", "cod"]):
        city = found_cities[0] if found_cities else "Bucuresti"
        data = get_weather(city)
        temp = data.get('temperature', 20)
        cond = remove_diacritics(data.get('condition', '').lower())
        
        if temp > 35: return f"Cod portocaliu de caniculă în {city} ({temp}°C)! Evită soarele."
        if temp < -10: return f"Alertă de ger în {city} ({temp}°C). Îmbracă-te foarte gros!"
        if any(x in cond for x in ["rain", "storm", "ploaie", "thunder"]):
            return f"Alertă de furtună sau precipitații în {city}. Asigură-te că ai adăpost!"
        return f"Momentan nu sunt raportate fenomene periculoase în {city}."

    # --- 4. PLANIFICATOR DE BAGAJ ---
    if any(word in clean_input for word in ["bagaj", "obiecte", "lista", "iau cu mine", "haine"]):
        city = found_cities[0] if found_cities else (user_profile.get('fav_city') if user_profile else "Bucuresti")
        data = get_weather(city)
        temp = data.get("temperature", 20)
        cond = remove_diacritics(data.get("condition", "").lower())
        
        items = ["Pașaport/ID", "Încărcător", "Baterie externă"]
        if temp < 10: items += ["Geacă grosă", "Căciulă", "Mănuși"]
        elif temp < 20: items += ["Hanorac", "Pantaloni lungi", "Jachetă ușoară"]
        else: items += ["Tricouri", "Pantaloni scurți", "Ochelari de soare"]
        
        if any(x in cond for x in ["rain", "ploaie", "shower", "drizzle"]):
            items += ["Umbrelă", "Pelerină"]

        return f"Lista pentru {city} ({temp}°C, {data.get('condition')}): {', '.join(items)}."

    # --- 5. RECOMANDĂRI ---
    if any(word in clean_input for word in ["recomanda", "unde sa merg", "vacanta", "sugestie"]):
        results = DESTINATIONS
        if "natura" in clean_input or "natura" in interests:
            results = [d for d in results if d["nature"] in ["munte", "padure", "vulcani"]]
        elif any(x in clean_input or x in interests for x in ["plaja", "soare", "mare"]):
            results = [d for d in results if d["type"] == "cald" and d["nature"] == "mare"]

        if results:
            top = results[:3]
            res_text = ", ".join([d["name"] for d in top])
            return f"Bazat pe preferințe, îți sugerez: {res_text}. Unde vrei să mergem?"

    # --- 6. INFO ORAȘ (Sfat implicit) ---
    if found_cities:
        data = get_weather(found_cities[0])
        if "error" not in data:
            advice = weather_message(data["temperature"], data["condition"])
            return f"În {found_cities[0]} sunt {data['temperature']}°C ({data['condition']}). {advice}"

    return "Salut! Te pot ajuta cu liste de bagaj, comparații între două orașe (ex: 'Compara Londra cu Paris') sau recomandări de vacanță."