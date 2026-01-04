# Proiect-IA4---WeatherLy

Titlu proiect: WeatherLy - Rain or Sun, we got you covered!

Tip: Aplicație meteo cu funcții personalizate, useri, joc

Descriere aplicație: 

WeatherLy este o aplicație meteo, ce oferă atât informații precise despre orașul căutat (precum coordonate temperatură, indice UV, etc), cât și date ușor de vizualizat, prin intermediul graficelor, hărților specifice fiecărui oraș în parte. Pe lângă toate funcționalitățile oferite pentru determinarea concretă a vremii într-un oraș anume, aplicația oferă și posibilitatea de autentificare pentru useri, aceștia având posibilitatea de a-și reține în cont informații importante, precum: orașe favorite, oraș principal, destinații de vis, etc. Aceste date pot fi găsite de fiecare user pe pagina dedicată, numită ,,Profil", vizibilă doar atunci când un user este logat.
Pagina ,,Orașe" cuprinde până la 450+ orașe importante ale lumii. Este, practic, o listă de orașe pentru care user-ul
poate accesa informațiile esențiale despre vreme la momentul respectiv.
În jurul acestei liste de orașe am creat WeatherBot-ul, un chatbot care poate comunica direct cu user-ul. Acest bot 
poate oferi sugestii de îmbrăcăminte, recomandări personalizate în funcție de vreme, date precise, precum și atracții 
turistice pentru anumite orașe, avertizări de vreme extremă sau comparare de orașe. Chatbot-ul are acces doar la datele metrice pentru orașele de pe pagină.
De asemenea, aplicația dispune de un joc numit ,,WeatherGame"- un joc animat care presupune colectarea de stele de către un soare și evitarea norilor ce vin pe direcția acestuia. Pentru fiecare stea se acumulează puncte, iar pentru fiecare nor se scad puncte. Dacă se ajunge la pragul superior de puncte, user-ul câștigă, iar dacă se ajunge la pragul inferior, user-ul pierde. Cât timp punctajul este între cele două praguri, jocul continuă.
Pe plan vizual, aplicația dispune și de buton de dark mode. Totodată, conține și o pagină de about, unde am scris despre aplicație.

Structura aplicației:

-> static: director ce cuprinde video și imagini, style.css
-> templates: director ce cuprinde paginile HTML efective ale aplicației (about_us.html, base.html, chatbot.html, index.html, login.html, minigame.html, more_details.html, popular_cities.html, register.html, settings.html)
-> sursele python: app.py, auth.py, chatbot.py, city_manager.py, utils.py, weather_data.py
-> documentația software .pdf (în engleză) - WeatherLy_Software_Architecture_Documentation.pdf
-> instance: director ce cuprinde, practic, baza de date a aplicației (weatherly.db), loc în care sunt reținuți userii după anumite date specifice, precum user, parolă (criptată), oraș favorit.
-> __pycache__

Modul de funcționare al aplicației:

Pagina principală a aplicației este menită căutării de orașe din întreaga lume (orice oraș ce poate fi furnizat de API).
Main-ul aplicației pornește by default cu datele oferite pentru București. De aici, utilizatorul poate vedea date avansate (localizare, date metrice precise, grafice de temperatură, umiditate, vânt), accesând butonul ,,Detalii avansate". În funcție de vremea la momentul respectiv (soare, nori, ploaie, ninsoare, etc.) fundalul aplicaței va fi
diferit, afișând o animație/un video ce corespunde cu starea vremii și temperatura la momentul căutării. De asemenea, pentru fiecare oraș căutat se oferă informații de localizare, precum latitudine, longitudine, continent. Tot în main, se găsește și butonul care dă accesul către jocul ,,WEATHERGAME", descris anterior.Tot aici, în partea dreaptă-jos, se regăsește chatbot-ul - WeatherBot, care salută user-ul conectat (sau un mesaj de bun-venit în caz că user-ul nu este logat) și așteaptă input-ul user-ului. Acesta oferă informații inteligente în funcție de datele primite, face recomandări, oferă informații interesante, curiozități. Are un meniu care poate fi accesat de către useri, prin diferite comenzi ('help' de exemplu), prin care se poate observa formularea cerută de acesta.
În navbar se regăsește buton pentru dark mode, buton de home, buton ce duce pe pagina cu orașe populare, aflată în corelație cu chatbot-ul, buton către pagina de about, buton de acces la profil în caz că user-ul este logat (și buton de logout), respectiv buton de login, dacă user-ul nu este încă logat. Pentru fiecare user, se rețin date precum orașul favorit, pentru a personaliza căutarea.
În funcție de vreme, aplicația oferă sfaturi personalizate (de exemplu:💡 Sfat: Scoate geaca de iarna de la naftalina. E rece afara). Accesând butonul ,,Detalii avansate", se trece pe ruta /more_details/<city>, unde se va regăsi  o pagină cu mai multe detalii, cu date precise despre starea curentă a vremii (intervale de temperatură, vânt, umiditate, localizare precisă).

Utilizări python3:

-> app.py: folosit pentru crearea instanței Flask și setarea cheii pentru sesiuni, gestionarea rutelor și a utilizatorilor, precum și stocarea acestora în baza de date folosind configuratorul SQLAlchemy și Flask-Login
-> utils.py: conține funcții utile folosite pentru rezolvarea anumitor funcționalități ale aplicației, precum: determinarea continentului în funcție de coordonate, generarea anumitor mesaje personalizate în funcție de anumiți paramentrii externi, precum indice UV sau temperatură
-> weather_data.py: este sursa de informație oferită de API. Aici, preluăm efectiv datele date de API și le stocăm într-un mod convenabil pentru a le folosi ulterior
-> city_manager.py: este, practic, o bază de date cu orașe importante, folosită de chatbot.
-> auth.py: folosit pentru reținerea userilor, modificarea/gestionarea bazei de date a aplicațiilor. Prin intermediul auth.py se adaugă useri în baza de date, fiind salvați după preferințele acestora.
-> chatbot.py: gestionează funcționarea chatbot-ului. Acesta preia datele pentru orașele importante, poate oferi informații despre vreme, despre obiective turistice, poate face recomandări inteligente de bagaje sau vestimentație, comparație între orașe pentru a-l face pe user să se decidă unde ar putea pleca.

Modul de lucru în echipă:

După ce am stabilit tema proiectului, am schițat cum ar trebui să arate în momentul în care am lucrat la documentația 
software. Atunci, am creat server-ul și principalele pagini html. Ulterior, am creat un proiect pe Github, cu 3 brach-uri, unul main și câte unul pentru fiecare dintre noi, acolo unde am urcat ce am lucrat în mod succesiv. Pe main
am adăugat întotdeauna lucrurile realizate la comun, după combinarea codului scris independent.
Link Github: https://github.com/SanduStefan/Proiect-IA4---WeatherLy/tree/main
Ne-am ocupat inițial de obținerea datelor prin intermediul unui API de vreme. Am reușit să obținem o cheie de acces pentru API-ul oferit de API_URL = "https://api.weatherapi.com/v1/current.json". Ulterior, am lucrat împreună la o primă versiune a aplicației, urmând ulterior să lucrăm independent pentru implementarea anumitor funcționalități pe care le-am stabilit înainte. La final, am combinat stilul, toate funcționalitățile, în varianta finală a aplicației.

Timp de implementare: 30-35 ore / membru

Membrii echipei:
Iosif Ianis-Cosmin, 321CC
Sandu Bogdan-Ștefan, 321CC