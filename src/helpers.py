import os
import csv
import time
import keyboard

def pressTabAndThenDownArrowUntil(counter):
    """Simula selección en menú desplegable."""
    for i in range(1, counter + 1):
        keyboard.press('tab' if i == 1 else 'down')
        time.sleep(random.uniform(0.2, 0.5))
    keyboard.press('enter')

def getAdsData():
    """Lee datos de anuncios desde CSV con manejo de errores."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, 'data', 'ads.csv')
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
            
    except FileNotFoundError:
        raise Exception("Archivo ads.csv no encontrado en la carpeta data")
    except Exception as e:
        raise Exception(f"Error leyendo archivo CSV: {str(e)}")