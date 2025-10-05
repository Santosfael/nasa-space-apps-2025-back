# Arquivo: repository.py (Versão final com o sufixo _temperatura)

import os
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

LOCATIONS = {
    "uberlandia": {"lat": -18.91, "lon": -48.27},
    "sao_paulo":  {"lat": -23.55, "lon": -46.63},
    "recife":     {"lat": -8.04,  "lon": -34.89}
}

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0; lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def _find_closest_city(lat, lon):
    if not lat or not lon: return None
    return min(LOCATIONS.keys(), key=lambda city: _haversine(lat, lon, LOCATIONS[city]['lat'], LOCATIONS[city]['lon']))

def get_daily_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        # <--- AJUSTE FINAL AQUI ---
        df = pd.read_csv(f'data/{city}_diarios_temperatura.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None

def get_hourly_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        # <--- AJUSTE FINAL AQUI ---
        df = pd.read_csv(f'data/{city}_horarios_temperatura.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None