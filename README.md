# Panneau Led Readme

Créée par: Zhou-efr
Date de création: 24 janvier 2023
Étiquette: ICE-EFREI

Repository pour le projet panneau LED de ICE EFREI. Ce projet permet de controller le panneau led de trois manières différentes : avec un arduino, une raspberry ou une STM32.

# Installation

## Raspberry

Pour compiler le code python sur votre raspberry vous devez d’abords installer les dépendances du projet :

```bash
pip install -r requirements.txt
```

Je recommande d’utiliser un environnement virtuel pour éviter les conflits de dépendances.
```bash
python3 -m venv ./venv/
source ./venv/bin/activate
```

En faisant attention à ce que la mention `(venv)` apparaisse dans votre terminal vous pouvez maintenant installer les dépendances avec la commande précédente.

## Arduino

Pour compiler le projet sur Arduino il faut télécharger les librairies suivantes depuis Arduino IDE ou directement sur github :

| Librairie | Lien |
| ------- | ------------------ |
| FastLED | https://fastled.io/ |
| arduinoFFT | https://github.com/kosme/arduinoFFT |

# Crédits

| Librairie | Lien |
| ------- | ------------------ |
| FastLED | https://fastled.io/ |
| arduinoFFT | https://github.com/kosme/arduinoFFT |
| Adafruit GFX Library | https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage |
| NeoMatrix |
| Adafruit NeoPixel |
| Tsun0 code | https://github.com/tsuno0/LEDdisplay |