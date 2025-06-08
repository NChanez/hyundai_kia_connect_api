from hyundai_kia_connect_api import *
from hyundai_kia_connect_api.const import BRAND_HYUNDAI, REGION_EUROPE
from datetime import datetime
import pandas as pd

def check_and_append_new_data(daily_stats, filename = 'daily_stats.csv'):
    df = pd.read_csv(filename,index_col=0)
    datas = [d.__dict__ for d in daily_stats]
    df.index = pd.to_datetime(df.index)
    df_new=pd.DataFrame(datas).set_index(df.index.name).loc[:,df.columns]
    combined_df = df.combine_first(df_new)
    combined_df.to_csv(filename)


USERNAME = 'nathanchanez@gmail.com'
PASSWORD = 'JHtx7Av!TCxxrVV'
REGION = 1
BRAND = 2

vm = VehicleManager(region=REGION, brand=BRAND, username=USERNAME, password=PASSWORD, pin='0619')
vm.check_and_refresh_token()
vm.update_all_vehicles_with_cached_state()
print(vm.vehicles)
daily_stats = vm.get_vehicle('f148cb56-d639-4ae4-964b-66a2f8c9539b').daily_stats

check_and_append_new_data(daily_stats)

vehicle = vm.get_vehicle('f148cb56-d639-4ae4-964b-66a2f8c9539b')

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
