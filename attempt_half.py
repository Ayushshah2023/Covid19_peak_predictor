import requests
import pandas as pd
import io
url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/key-countries-pivoted.csv"
s = requests.get(url).content
global_data = pd.read_csv(io.StringIO(s.decode('utf-8')))
print(global_data)

global_data.to_csv("AttemptKaCSV.csv")
