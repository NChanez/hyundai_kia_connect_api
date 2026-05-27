import os
from datetime import datetime

from hyundai_kia_connect_api import *
from hyundai_kia_connect_api.const import BRAND_HYUNDAI, REGION_EUROPE
import pandas as pd


def check_and_append_new_data(daily_stats, filename='daily_stats.csv'):
    # Transformer les objets en dicts
    datas = [d.__dict__ for d in daily_stats]
    df_new = pd.DataFrame(datas)

    # S'assurer qu'on a une colonne date pour l'index
    # Remplacez 'date' par le nom réel de votre champ date dans daily_stats
    if 'date' not in df_new.columns:
        raise ValueError("La colonne 'date' est absente dans daily_stats")
    df_new['date'] = pd.to_datetime(df_new['date'])
    df_new = df_new.set_index('date').sort_index()

    # Charger l'existant s'il existe, sinon créer vide
    try:
        df = pd.read_csv(filename, index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index)
    except FileNotFoundError:
        df = pd.DataFrame().set_index(df_new.index.name)

    # Aligner les colonnes: union pour ne rien perdre
    all_cols = sorted(set(df.columns).union(df_new.columns))
    df = df.reindex(columns=all_cols)
    df_new = df_new.reindex(columns=all_cols)

    # Mettre à jour (écraser) les valeurs existantes avec les nouvelles
    df_updated = df.copy()
    df_updated.update(df_new)

    # Ajouter les nouvelles dates qui n'existaient pas
    to_append = df_new.loc[~df_new.index.isin(df_updated.index)]
    combined_df = pd.concat([df_updated, to_append]).sort_index()

    combined_df.to_csv(filename)

def required_env(name):
    """Read a required local secret without storing it in the Git repository."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


USERNAME = required_env("HYUNDAI_KIA_USERNAME")
PASSWORD = required_env("HYUNDAI_KIA_PASSWORD")
PIN = required_env("HYUNDAI_KIA_PIN")
VEHICLE_ID = required_env("HYUNDAI_KIA_VEHICLE_ID")
REGION = int(os.getenv("HYUNDAI_KIA_REGION", "1"))
BRAND = int(os.getenv("HYUNDAI_KIA_BRAND", "2"))

vm = VehicleManager(region=REGION, brand=BRAND, username=USERNAME, password=PASSWORD, pin=PIN)
vm.check_and_refresh_token()
vm.update_all_vehicles_with_cached_state()
print(vm.vehicles)
daily_stats = vm.get_vehicle(VEHICLE_ID).daily_stats

check_and_append_new_data(daily_stats)

vehicle = vm.get_vehicle(VEHICLE_ID)

# for year in [2024, 2025]:
#     for month in [4, 5, 6, 7, 8, 9, 10, 11, 12]:
#         now = datetime(year, month, 1)
#
#         yyyymm = now.strftime("%Y%m")
#         yyyymmdd = now.strftime("%Y%m%d")
#         vm.update_month_trip_info(vehicle.id, yyyymm)
#         if vehicle.month_trip_info is not None:
#             print(f'Year : {year}, Month : {month}')
#             print(vehicle.month_trip_info)
