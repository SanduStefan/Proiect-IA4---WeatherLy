def get_uv_advice(uv):
    if uv <= 2: return "UV scăzut. Totul e sigur."
    if uv <= 5: return "UV moderat. Poartă ochelari de soare."
    return "UV ridicat! Aplică cremă cu protecție solară."

def weather_message(temp, condition):
    cond = condition.lower()
    advice = ""

    is_raining = any(x in cond for x in ["rain", "ploaie", "drizzle", "grindina", "shower", "burniță", "ploi"])
    rain_advice = " Neapărat ia o umbrelă sau o pelerină!" if is_raining else ""
    
    if temp < -15:
        advice = "E un ger cumplit afara! Evita iesirile neesentiale din casa"
    elif -15 <= temp < 0:
        advice = "E foarte frig! Geacă groasă, fular și mănuși neapărat. 🥶"
    elif 0 <= temp < 5:
        advice = "Scoate geaca de iarna de la naftalina. E rece afara."
    elif 5 <= temp < 15:
        advice = "Destul de răcoare. O jachetă de toamnă sau un palton e ideal. 🧥"
    elif 15 <= temp < 22:
        advice = "Vreme perfectă! Un hanorac sau o geacă de piele e suficientă. 👕"
    elif 22 <= temp < 30:
        advice = "E cald și bine! Tricou și haine lejere de bumbac. 👕"
    else:
        advice = "Caniculă! Haine cât mai subțiri, deschise la culoare, șapcă și multă apă. ☀️"

    if "zăpadă" in cond or "snow" in cond:
        advice += " Atenție la polei, ia încălțări cu talpă aderentă! 🥾"
        
    return advice + rain_advice

def get_continent(lat, lon):
    if lat >= 7 and lat <= 83 and lon >= -170 and lon <= -50:
        return "America de Nord"
    elif lat >= -55 and lat <= 12 and lon >= -81 and lon <= -35:
        return "America de Sud"
    elif lat >= 36 and lat <= 71 and lon >= -10 and lon <= 60:
        return "Europa"
    elif lat >= -35 and lat <= 37 and lon >= -17 and lon <= 51:
        return "Africa"
    elif lat >= -1 and lat <= 77 and lon >= 26 and lon <= 180:
        return "Asia"
    elif lat >= -47 and lat <= 0 and lon >= 110 and lon <= 180:
        return "Oceania"
    elif lat <= -60:
        return "Antarctica"
    return "Necunoscut / Ocean"