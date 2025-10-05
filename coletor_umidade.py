import netrc
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import io
import os
import numpy as np

lat = -18.91
lon = -48.24
cidade_nome_arquivo = 'uberlandia'

time_start = "2000-01-01T00:00:00"
time_end = "2024-09-30T21:00:00"

data = "GLDAS_NOAH025_3H_2_1_Qair_f_inst"

signin_url = "https://api.giovanni.earthdata.nasa.gov/signin"
creds = netrc.netrc().authenticators('urs.earthdata.nasa.gov')
if creds is None:
    raise RuntimeError("Credenciais Earthdata não encontradas em ~/.netrc!")
user, _, pwd = creds
token = requests.get(signin_url, auth=HTTPBasicAuth(user, pwd), allow_redirects=True).text.replace('"','')


def call_time_series(lat, lon, time_start, time_end, data, token):
    query_parameters = {
        "data": data,
        "location": f"[{lat},{lon}]",
        "time": f"{time_start}/{time_end}"
    }
    headers = {"authorizationtoken": token}
    response = requests.get("https://api.giovanni.earthdata.nasa.gov/timeseries",
                            params=query_parameters, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Erro na requisição: HTTP {response.status_code} - {response.text[:300]}")
    return response.text

csv_text = call_time_series(lat, lon, time_start, time_end, data, token)

lines = csv_text.splitlines()
header_index = next(i for i, line in enumerate(lines) if line.strip().lower().startswith("timestamp (utc),"))
table_csv = "\n".join(lines[header_index:])
df = pd.read_csv(io.StringIO(table_csv))

df.replace(-9999.0, np.nan, inplace=True)

df['time'] = pd.to_datetime(df.iloc[:, 0])
df.set_index('time', inplace=True)

df.rename(columns={'Data': 'specific_humidity_kg_kg'}, inplace=True)

os.makedirs('data', exist_ok=True)

hourly_df = df[['specific_humidity_kg_kg']].dropna()
output_hourly = f'data/{cidade_nome_arquivo}_horarios_umidade.csv'
hourly_df.to_csv(output_hourly)
print(f"-> Arquivo com dados de umidade (a cada 3h) salvo em: {output_hourly}")

daily_df = df.resample('D').agg(
    humidity_avg_kg_kg=('specific_humidity_kg_kg', 'mean')
)
    
final_daily_df = daily_df.dropna()
output_daily = f'data/{cidade_nome_arquivo}_diarios_umidade.csv'
final_daily_df.to_csv(output_daily)
print(f"-> Arquivo com dados diários de umidade salvo em: {output_daily}")