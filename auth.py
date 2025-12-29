# Simulare bază de date utilizatori (în producție se folosește o bază de date reală)
USERS = {
    "admin": "parola123",
    "student": "proiect2025",
    "user": "weather"
}

def check_user(username, password):
    """Verifică dacă perechea user/parolă este corectă."""
    if username in USERS and USERS[username] == password:
        return True
    return False

def register_user(username, password):
    """Adaugă un utilizator nou (valabil doar pe durata rulării serverului în acest demo)."""
    if username in USERS:
        return False, "Utilizatorul există deja."
    USERS[username] = password
    return True, "Cont creat cu succes."