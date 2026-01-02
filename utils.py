def get_uv_advice(uv):
    if uv <= 2: return "UV scăzut. Totul e sigur."
    if uv <= 5: return "UV moderat. Poartă ochelari de soare."
    return "UV ridicat! Aplică cremă cu protecție solară."

def weather_message(temp, condition):
    cond = condition.lower()
    advice = ""

    is_raining = any(x in cond for x in ["rain", "ploaie", "drizzle", "grindina", "shower", "burniță"])
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