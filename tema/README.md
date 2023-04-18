Nume: Baicu Bogdan Alexandru
Grupa: 333CC

#Tema 1 TODO
Tema consta în implementarea unui marketplace bazat pe paradigma Multiple Producers Multiple Consumers,
folosind Python și multi-threading.
Am abordat tema începând prin implementarea metodelor din clasa marketplace. Aceasta conținea metodele 
"principale", utilizate apoi de clasele producer si consumer.
La bază am folosit 2 dicționare, unul pentru coșul de cumpărături si unul pentru producători. In dicționarul
coșului de cumpărături, cheia era id-ul coșului, iar valoarea era o listă formată din perechi produs-producător.
În dicționarul producătorilor, cheia era id-ul producătorului, iar valoarea era lista de produse.
Id-urile pentru coș era reprezentat de numărul de coșuri de cumpărături existe (numerotarea incepea de la 0). 
Pentru producători am procedat asemănător, doar că id-ul era de această datp un string format din "prod" și 
numărul de producători existenți (deci primul producător avea id-ul "prod0").
Am folosit 3 lock-uri: unul pentru crearea producătorilor, unul pentru crearea coșului de cumpărături și un al 
treilea pentru restul operațiunilor asupra coșului de cumpărături. Primele 2 lock-uri au fost folosite pentru
a evita race condition în cazul în care mai multe thread-uri încearcă sa creeze coșuri de cumpărături sau producători
simultan, fapt ce ar putea produce id-uri duplicate. Lock-ul pentru restul operațiunilor asupra coșului de cumpărături
a fost folosit pentru a mă asigura că 2 sau mai multe thread-uri nu pot modifica simultan cosul de cumpărături, ceea ce
ar duce de asemenea la race condition.
Am folosit try-except pentru a prinde exceptii si a le nota in fisierul marketplace.log.
Am respectat condițiile impuse în enunțul temei, referitoare la disponibilitatea produselor, numărul maxim de elemente 
ce pot fi publicate și timpii de așteptare până la republicare sau căutarea din nou a unui produs.
Consider că tema a fost utilă, ajutându-mă să îmi dezvolt atât skill-urile legate de Python, și să
înțeleg mai bine paradigma MPMC.
Consider că implementarea este una destul de eficientă.

###Implementare
Am implementat întreaga temă.
O dificultate întâmpinată a fost legată de consigurarea logging-ului, având drept consecință fișiere de logging 
goale, însă am rezolvat problema prin adăugarea parametrului "level". 

###Resurse utilizate
Principala resursă utilizată a fost laboratorul 2. Pe lângă acesta, am folosit și link-urile către documentația 
Python pentru Unittesting și Logging oferite pe pagina de OCW a temei.

###Git
https://github.com/BogdanBaicu/Marketplace-Python