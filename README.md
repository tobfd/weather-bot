# Wetter Discord Bot

Der Bot ist in Python mit py-cord und ezcord programmiert wurden.

<img height="128" src=".github/weather.png" width="128"/>

## Testen
Ihr könnt den Bot auf eurem Server einladen und testen mit dem folgendem [Link](https://discord.com/oauth2/authorize?client_id=1262014442326069288).
## Funktionen
Mit ```/weather``` können Informationen über das Wetter abgerufen werden darunter sind:
- Temperatur
- gefühlte Temperatur
- Luftfeuchtigkeit
- Wind Geschwindigkeit
- Sonnenaufgang
- Sonnenuntergang
- Ein Bild mit der Wettersituation
- Eine Beschreibung der Wetterlage

dann noch dasselbe für die nächsten 3 Stunden.
Hier ein Bild vom Command:  
<img src=".github/command.png">  
Und dann noch in den Nächsten 3 Stunden:  
<img src=".github/three_hours.png">

Man kann per Button immer wieder von der jetzigen Wettervorhersage zur der in den nächsten 3 Stunden springen.

Der Bot wurde im Zusammenhang mit dem Hackathon von [Kevin Chromik](https://www.youtube.com/@KevinChromik) erstellt.

## Installation
1.
````
pip install -r requirements.txt
````
2.  
Eine ``.env`` erstellen und Token aus dem Discord Developer Portal einfügen und den API KEY von OPWM siehe ``.env.example``.  
3.
DIe ``main.py`` starten.

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/tobfd/weather-bot">Weather Bot</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/tobfd">Tobias Schmitt</a> is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a></p>
