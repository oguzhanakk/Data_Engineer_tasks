import pandas as pd
import numpy as np
import numpy.random as random

kolonlar = ["id","isim","soyisim","yas","alacak","verecek","meslek"]
df = pd.DataFrame(columns=kolonlar)

for x in range(1,10):
    df = df.append({
        "id":"10" + str(x),
    }, ignore_index=True)

print(df)
df.to_excel("deneme_excel.xlsx")