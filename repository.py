import os
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

LOCATIONS = {
    "uberlandia": {"lat": -18.91, "lon": -48.27},
    "sao_paulo":  {"lat": -23.55, "lon": -46.63},
}

def _haversine(lat1, lon1, lat2, lon2):
    R = 6371.0; lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def _find_closest_city(lat, lon):
    if not lat or not lon: return None
    return min(LOCATIONS.keys(), key=lambda city: _haversine(lat, lon, LOCATIONS[city]['lat'], LOCATIONS[city]['lon']))

def get_daily_temperature_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        df = pd.read_csv(f'data/{city}_diarios_temperatura.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None

def get_hourly_temperature_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        df = pd.read_csv(f'data/{city}_horarios_temperatura.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None
    
def get_daily_precipitation_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        df = pd.read_csv(f'data/{city}_diarios_precipitacao.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None
    
def get_hourly_precipitation_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        df = pd.read_csv(f'data/{city}_horarios_precipitacao.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None
    
def get_daily_humidity_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        df = pd.read_csv(f'data/{city}_diarios_umidade.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None

def get_hourly_humidity_data(lat, lon):
    city = _find_closest_city(lat, lon)
    if not city: return None, None
    try:
        df = pd.read_csv(f'data/{city}_horarios_umidade.csv', index_col='time', parse_dates=True)
        return df, city
    except FileNotFoundError:
        return None, None