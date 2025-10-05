# Arquivo: service.py (Versão final com 4 categorias e destaque da maior probabilidade)

import repository
from datetime import datetime

# --- Função auxiliar para encontrar a maior probabilidade ---
def _find_most_likely(all_results):
    if not all_results or "error" in all_results:
        return all_results
    most_likely_key = max(all_results, key=lambda k: float(all_results[k]['probability'].replace('%','')))
    return {
        "most_likely_condition": most_likely_key,
        "full_analysis": all_results
    }

# --- LÓGICA DE ANÁLISE DIÁRIA ---
def get_daily_analysis(lat: float, lon: float, date_str: str):
    df, city_name = repository.get_daily_data(lat, lon)
    if df is None:
        return {"error": f"No pre-calculated data found near lat={lat}, lon={lon}."}, None

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
    except (ValueError, TypeError): 
        return {"error": "Invalid date format. Use YYYY-MM-DD."}, city_name

    target_day_data = df[(df.index.day == target_date.day) & (df.index.month == target_date.month)]
    if target_day_data.empty: 
        return {"error": f"No historical data found for {target_date.month}/{target_date.day}."}, city_name

    total_years = len(target_day_data)
    all_results = {}

    p10_min, p30_min = (df['temp_min_c'].quantile(q) for q in [0.10, 0.30])
    p70_max, p90_max = (df['temp_max_c'].quantile(q) for q in [0.70, 0.90])
    
    all_results["Very Cold"] = {"threshold": f"Min Temp < {p10_min:.1f}°C", "probability": f"{(target_day_data[target_day_data['temp_min_c'] < p10_min].shape[0] / total_years) * 100:.1f}%"}
    all_results["Cold"] = {"threshold": f"Min Temp between {p10_min:.1f}°C and {p30_min:.1f}°C", "probability": f"{(target_day_data[target_day_data['temp_min_c'].between(p10_min, p30_min)].shape[0] / total_years) * 100:.1f}%"}
    all_results["Hot"] = {"threshold": f"Max Temp between {p70_max:.1f}°C and {p90_max:.1f}°C", "probability": f"{(target_day_data[target_day_data['temp_max_c'].between(p70_max, p90_max)].shape[0] / total_years) * 100:.1f}%"}
    all_results["Very Hot"] = {"threshold": f"Max Temp > {p90_max:.1f}°C", "probability": f"{(target_day_data[target_day_data['temp_max_c'] > p90_max].shape[0] / total_years) * 100:.1f}%"}
    
    return _find_most_likely(all_results), city_name

# --- LÓGICA DE ANÁLISE HORÁRIA ---
def get_hourly_analysis(lat: float, lon: float, date_str: str, hour: int):
    df, city_name = repository.get_hourly_data(lat, lon)
    if df is None:
        return {"error": f"No pre-calculated hourly data found near lat={lat}, lon={lon}."}, None
    
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        target_hour = int(hour)
    except (ValueError, TypeError): 
        return {"error": "Invalid date or hour parameters."}, city_name

    closest_hour = min([0, 3, 6, 9, 12, 15, 18, 21], key=lambda x: abs(x - target_hour))
    all_results = {}
    target_data = df[(df.index.day == target_date.day) & (df.index.month == target_date.month) & (df.index.hour == closest_hour)]
                     
    if target_data.empty: 
        return {"error": f"No historical data for {target_date.month}/{target_date.day} at {closest_hour}h."}, city_name

    total_years = len(target_data)
    p10_hr, p30_hr, p70_hr, p90_hr = (df['temp_c'].quantile(q) for q in [0.10, 0.30, 0.70, 0.90])

    all_results["Very Cold"] = {"threshold": f"Temp at {closest_hour}h < {p10_hr:.1f}°C", "probability": f"{(target_data[target_data['temp_c'] < p10_hr].shape[0] / total_years) * 100:.1f}%"}
    all_results["Cold"] = {"threshold": f"Temp at {closest_hour}h between {p10_hr:.1f}°C and {p30_hr:.1f}°C", "probability": f"{(target_data[target_data['temp_c'].between(p10_hr, p30_hr)].shape[0] / total_years) * 100:.1f}%"}
    all_results["Hot"] = {"threshold": f"Temp at {closest_hour}h between {p70_hr:.1f}°C and {p90_hr:.1f}°C", "probability": f"{(target_data[target_data['temp_c'].between(p70_hr, p90_hr)].shape[0] / total_years) * 100:.1f}%"}
    all_results["Very Hot"] = {"threshold": f"Temp at {closest_hour}h > {p90_hr:.1f}°C", "probability": f"{(target_data[target_data['temp_c'] > p90_hr].shape[0] / total_years) * 100:.1f}%"}
    
    return _find_most_likely(all_results), city_name