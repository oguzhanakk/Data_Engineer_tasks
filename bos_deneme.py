import numpy as np
import pandas as pd

df = pd.read_excel("tum_ykv_birlesim.xlsx")
column_names = df.columns.values

m = df[column_names[40]].values.tolist()
df_yeni = pd.DataFrame(m, columns=["var1"])
print(df_yeni)

print(df_yeni)