import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

pd.set_option('display.max_rows', 1000)

url = "https://www.disastercenter.com/crime/uscrime.htm"
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")

table_data = soup.select('table[style*="background-color: rgb(255, 255, 255);"]')
table_data_rows = []
table_data_row_values = []

for row in table_data:
    row_list = row.find_all(attrs={"size": "-1"})
    table_data_rows.append(row_list)

for cell in row_list:
    table_data_row_values.append(cell.text)

df = pd.DataFrame(table_data_row_values)

all_num_values = []

for i, data in enumerate(df[0]):
    try:
        data = float(data.replace(',',''))
        all_num_values.append(data)
    except:
        print("non floatable")

all_num_values_formated = np.array_split(all_num_values, 50)
formated_df_columns = {'year': [], 'population':[], 'total': [], 'violent': [], 'property': [], 'murder': [], 'forcible_rape': [], 'roberry': [], 'agravated_assault': [], 'burglary': [], 'larcency_theft': [], 'vehicle_theft': []}

formated_df = pd.DataFrame(all_num_values_formated, columns = formated_df_columns)

final_table = soup.select("td > small")
num_values = []
formated_num_values = []

for cell in final_table:
    num_values.append(cell.text)

num_values = np.array_split(num_values, 2)

for i, value in enumerate(num_values[1]):
    try:
        value = value.replace(',','')
        value = value.replace('*','')
        value = float(value)
        formated_num_values.append(value)
    except:
        print()

formated_num_values = np.array_split(formated_num_values, 10)

indexes_arr = []

for i in range(50, 60): indexes_arr.append(i)

print(indexes_arr)

final_df = pd.DataFrame(formated_num_values, columns = formated_df_columns, index= indexes_arr)

formated_df = formated_df.append(final_df)

formated_df = formated_df.astype({'year':int})
formated_df = formated_df.set_index('year')

formated_df_json = formated_df.to_json(orient='index')
formated_df_parsed_json = json.loads(formated_df_json)
json.dumps(formated_df_parsed_json, indent=4)

print(formated_df_json)

with open('us-crime-data.json', 'w', encoding='utf-8') as file: 
    json.dump(formated_df_json, file)