import numpy as np
import pandas as pd

#excell verilerini dataframe'e dondurmek.
df = pd.read_excel("tum_ykv_birlesim.xlsx")

#0.satirdaki sutun basliklarini almak.
column_names = df.columns.values

tum_veriler = []
tum_veriler = df["Ekim"].values.tolist() + df["Aralık"].values.tolist()

#print(df[column_names[0],column_names[3]])

listeler = []
for i in range(0,49):
    if(i == 40 or i == 41):
        continue
    listeler += df[column_names[i]].values.tolist()

list_no_nan = [x for x in listeler if pd.notnull(x)]
print(len(list_no_nan))

gecici_kume = set(list_no_nan)
tum_veriler_essiz = list(gecici_kume)

print(len(tum_veriler_essiz))

















