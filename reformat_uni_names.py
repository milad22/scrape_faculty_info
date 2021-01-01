import pandas as pd
import re

unis_dataframe = pd.read_excel('Physics_departments_original.xlsx', na_values = 'None')
for index, row in unis_dataframe.iterrows():
    uni = row['University']
    uni = uni.replace('-','')
    uni = uni.replace('–','')
    uni = uni.replace(',','')
    uni = re.sub(r"\s+", '_', uni)
    row['University'] = uni

unis_dataframe.to_excel('Physics_departments_formatted.xlsx', index=False)