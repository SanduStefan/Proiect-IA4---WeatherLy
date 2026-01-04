import unicodedata
import wikipedia

from city_manager import DESTINATIONS, TOP_CITIES
from weather_data import get_weather
from utils import weather_message

wikipedia.set_lang("ro")



def remove_diacritics(text):
    if not text:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )



CITY_ALIASES = {
    "bucuresti": "Bucharest",
    "bucharest": "Bucharest"
}

def resolve_city(city):
    key = remove_diacritics(city.lower())
    return CITY_ALIASES.get(key, city)



def city_not_found_message():
    return (
        "Orasul nu exista in lista. "
        "Poți verifica lista completă aici: "
        "<a href='/popular_cities'>Lista de orașe</a>"
    )


def get_tourist_attractions(city):

    search_queries = [
        f"{city} turism",
        f"atractii turistice {city}",
        f"obiective turistice {city}",
        f"vizitare {city}",
        city
    ]

    tourism_keywords = [
        "atrac", "turis", "vizit", "obiectiv", "muzeu",
        "parc", "palat", "castel", "centru vechi",
        "monument", "biseric", "catedral"
    ]

    for query in search_queries:
        try:
            page = wikipedia.page(query, auto_suggest=False)
            summary = page.summary.lower()

            if any(k in summary for k in tourism_keywords):
                sentences = page.summary.split(".")
                tourism_sentences = [
                    s.strip() for s in sentences
                    if any(k in s.lower() for k in tourism_keywords)
                ]
                if tourism_sentences:
                    return ". ".join(tourism_sentences[:4]).strip() + "."
            
                return ". ".join(sentences[:3]).strip() + "."
        except:
            continue

    return "Nu s-au găsit date despre căutarea ta."


def options_message():
    return (
        "🤖 Pot răspunde la următoarele tipuri de cereri:\n\n"
        "--- Informații meteo pentru un oraș\n\n"
        "(Ex: \"Vremea în Oslo\")\n\n"
        "--- Comparații între două orașe\n\n"
        "(Ex: \"Compara Londra cu Paris\")\n\n"
        "--- Alerte meteo extreme\n\n"
        "(Ex: \"Alertă Roma\")\n\n"
        "--- Listă de bagaj\n\n"
        "(Ex: \"Ce iau cu mine în Berlin?\")\n\n"
        "--- Recomandări de vacanță\n\n"
        "(Ex: \"Recomandă o destinație de vacanță la mare\")\n\n"
        "--- Atracții turistice (opțiune valabilă doar pentru anumite orașe)\n\n"
        "(Ex: \"Turism Brașov\" sau \"Turism Praga\") ---"
    )



def get_chatbot_response(user_input, user_profile=None):
    raw_input = user_input.lower()
    clean_input = remove_diacritics(raw_input)
    interests = remove_diacritics(user_profile.get('interests', '').lower()) if user_profile else ""

   
    if "info orase" in clean_input:
        return (
            "🤖 Chatbotul are informații despre peste 400 de orașe, "
            "care se pot găsi aici: <a href='/popular_cities'>Lista de orașe</a>"
        )
    
    if any(word in clean_input for word in ["optiuni", "optiune", "ajutor", "help"]):
        return options_message()

    
    found_cities = []
    sorted_cities = sorted(TOP_CITIES, key=len, reverse=True)
    for city in sorted_cities:
        city_clean = remove_diacritics(city.lower())
        if city_clean in clean_input and city not in found_cities:
            found_cities.append(city)
            clean_input = clean_input.replace(city_clean, "", 1)

    
    for alias, target in CITY_ALIASES.items():
        if alias in clean_input and target not in found_cities:
            found_cities.append(target)
            clean_input = clean_input.replace(alias, "", 1)


    if any(word in clean_input for word in ["vremea", "cum e vremea", "meteo"]):
        if not found_cities:
            return city_not_found_message()
        city = found_cities[0]
        if city not in TOP_CITIES:
            return city_not_found_message()
        data = get_weather(resolve_city(city))
        if not data or "error" in data:
            return city_not_found_message()
        advice = weather_message(data["temperature"], data["condition"])
        return f"În {city} sunt {data['temperature']}°C ({data['condition']}). {advice}"


    if any(word in clean_input for word in ["atractii turistice", "atractii", "obiective turistice", "turism"]):
        if not found_cities:
            return city_not_found_message()
        city = found_cities[0]
        info = get_tourist_attractions(city)
        return f"Atracții turistice în {city}:\n{info}"


    if len(found_cities) >= 2 and any(word in clean_input for word in ["compara", "fata de", "vs", "versus"]):
        c1, c2 = found_cities[0], found_cities[1]
        if c1 not in TOP_CITIES or c2 not in TOP_CITIES:
            return city_not_found_message()
        w1, w2 = get_weather(resolve_city(c1)), get_weather(resolve_city(c2))
        if not w1 or "error" in w1:
            return "Nu detin informatii despre primul oraș..."
        if not w2 or "error" in w2:
            return "Nu detin informatii despre al doilea oraș..."
        t1, t2 = w1['temperature'], w2['temperature']
        diff = abs(t1 - t2)
        better = c1 if t1 > t2 else c2
        return (
            f"Analiză comparativă: În {c1} sunt {t1}°C, iar în {c2} sunt {t2}°C. "
            f"Diferența este de {diff}°C. Dacă preferi căldura, {better} este alegerea mai bună!"
        )


    if any(word in clean_input for word in ["alerta", "pericol", "furtuna", "extrem", "cod"]):
        if not found_cities:
            return city_not_found_message()
        city = found_cities[0]
        if city not in TOP_CITIES:
            return city_not_found_message()
        data = get_weather(resolve_city(city))
        if not data or "error" in data:
            return city_not_found_message()
        temp = data.get('temperature', 20)
        cond = remove_diacritics(data.get('condition', '').lower())
        if temp > 35:
            return f"Cod portocaliu de caniculă în {city} ({temp}°C)! Evită soarele."
        if temp < -10:
            return f"Alertă de ger în {city} ({temp}°C). Îmbracă-te foarte gros!"
        if any(x in cond for x in ["rain", "storm", "ploaie", "thunder"]):
            return f"Alertă de furtună sau precipitații în {city}. Asigură-te că ai adăpost!"
        return f"Momentan nu sunt raportate fenomene periculoase în {city}."


    if any(word in clean_input for word in ["bagaj", "obiecte", "lista", "iau cu mine", "haine"]):
        if not found_cities:
            return city_not_found_message()
        city = found_cities[0]
        if city not in TOP_CITIES:
            return city_not_found_message()
        data = get_weather(resolve_city(city))
        if not data or "error" in data:
            return city_not_found_message()
        temp = data.get("temperature", 20)
        cond = remove_diacritics(data.get("condition", "").lower())
        items = ["Pașaport/ID", "Încărcător", "Baterie externă"]
        if temp < 10:
            items += ["Geacă grosă", "Căciulă", "Mănuși"]
        elif temp < 20:
            items += ["Hanorac", "Pantaloni lungi", "Jachetă ușoară"]
        else:
            items += ["Tricouri", "Pantaloni scurți", "Ochelari de soare"]
        if any(x in cond for x in ["rain", "ploaie", "shower", "drizzle"]):
            items += ["Umbrelă", "Pelerină"]
        return f"Lista pentru {city} ({temp}°C, {data.get('condition')}): {', '.join(items)}."

  
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


    if found_cities:
        city = found_cities[0]
        if city not in TOP_CITIES:
            return city_not_found_message()
        data = get_weather(resolve_city(city))
        if not data or "error" in data:
            return city_not_found_message()
        advice = weather_message(data["temperature"], data["condition"])
        return f"În {city} sunt {data['temperature']}°C ({data['condition']}). {advice}"

 
    examples = [
        "Ce iau cu mine în Londra?",
        "Compara Oslo cu Paris",
        "Alertă în Roma",
        "Recomanda o destinație de vacanță la mare",
        "Lista pentru bagaj în Berlin",
        "Atracții Brașov"
    ]
    example_text = "\n• " + "\n• ".join(examples)
    return (
        "⚠️ Nu am găsit un răspuns concret pentru mesajul tău.\n"
        "Poți încerca unul dintre următoarele exemple:\n" + example_text
    )