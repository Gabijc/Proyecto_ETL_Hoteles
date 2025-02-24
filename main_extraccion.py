# Importamos las librerías necesarias
import pandas as pd 
import numpy as np 
import requests
from selenium import webdriver # esto nos permite controlar navegadores web mediante código
from webdriver_manager.chrome import ChromeDriverManager # administra la instalación de chromedriver, que es necesario para controlar google chrome
from selenium.webdriver.chrome.service import Service # permite gestionar el servicio del driver de chrome
import time
from src.soporte_extraccion import scrapeo_competencia, eventos_api

url_ibis = "https://all.accor.com/ssr/app/ibis/hotels/madrid-spain/open/index.es.shtml?compositions=1&stayplus=false&snu=false&hideWDR=false&accessibleRooms=false&hideHotelDetails=false&dateIn=2025-03-01&nights=1&destination=madrid-spain"

enp = f"https://datos.madrid.es/egob/catalogo/300107-0-agenda-actividades-eventos.json"

if __name__ == "__main__":
    scrapeo_competencia(url_ibis)
    eventos_api(enp)