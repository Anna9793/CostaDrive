import urllib.request
import json

def _fetch_json(url):
    """Universal helper to fetch and parse JSON from a URL."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read().decode())

def obtener_precios_carburante_alicante():
    """
    Obtiene los precios de combustible oficiales de la API del Ministerio
    para la provincia de Alicante (ID: 03) y calcula el precio medio actual
    para Gasolina 95 E5 y Gasóleo A (Diésel).
    """
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroProvincia/03"
    try:
        data = _fetch_json(url)
        stations = data.get('ListaEESSPrecio', [])
        
        g95_prices = []
        diesel_prices = []
        
        for s in stations:
            g95_val = s.get('Precio Gasolina 95 E5', '').replace(',', '.')
            diesel_val = s.get('Precio Gasoleo A', '').replace(',', '.')
            
            if g95_val:
                try:
                    g95_prices.append(float(g95_val))
                except ValueError:
                    pass
            if diesel_val:
                try:
                    diesel_prices.append(float(diesel_val))
                except ValueError:
                    pass
        
        avg_g95 = sum(g95_prices) / len(g95_prices) if g95_prices else 0.0
        avg_diesel = sum(diesel_prices) / len(diesel_prices) if diesel_prices else 0.0
        
        return {
            'success': True,
            'avg_g95': round(avg_g95, 3),
            'avg_diesel': round(avg_diesel, 3),
            'total_stations': len(stations),
            'fecha': data.get('Fecha', 'Hoy')
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def obtener_tiempo_denia():
    """
    Obtiene el clima actual de Dénia (Alicante) desde la API de Open-Meteo.
    """
    url = "https://api.open-meteo.com/v1/forecast?latitude=38.8408&longitude=0.1057&current_weather=true"
    try:
        data = _fetch_json(url)
        cw = data.get('current_weather', {})
        temp = cw.get('temperature', 0.0)
        code = cw.get('weathercode', 0)
        wind = cw.get('windspeed', 0.0)
        
        interpretaciones = {
            0: ("Despejado", "☀️"),
            1: ("Mayormente despejado", "🌤️"),
            2: ("Nublado", "⛅"),
            3: ("Cubierto", "☁️"),
            45: ("Niebla", "🌫️"),
            48: ("Niebla helada", "🌫️"),
            51: ("Llovizna ligera", "🌧️"),
            53: ("Llovizna moderada", "🌧️"),
            55: ("Llovizna intensa", "🌧️"),
            61: ("Lluvia débil", "🌧️"),
            63: ("Lluvia moderada", "🌧️"),
            65: ("Lluvia fuerte", "🌧️"),
            80: ("Chubascos débiles", "🌦️"),
            81: ("Chubascos moderados", "🌦️"),
            82: ("Chubascos violentos", "⛈️"),
            95: ("Tormenta eléctrica", "⚡")
        }
        desc, emoji = interpretaciones.get(code, ("Desconocido", "🌡️"))
        
        return {
            'success': True,
            'temp': temp,
            'desc': desc,
            'emoji': emoji,
            'wind': wind
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
