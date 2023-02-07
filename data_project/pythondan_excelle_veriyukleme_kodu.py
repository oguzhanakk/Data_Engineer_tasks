import pandas as pd
import numpy as np
import numpy.random as random

kolonlar = ["id","isim","soyisim","yas","alacak","verecek","meslek"]
df = pd.DataFrame(columns=kolonlar)
isimler = ["Çağlar","Çağla","Onur","Reyhan","Özgür","Dilara","Ezgi","Emre","Gökhan","Gizem"]
soyisimler = ["Öztürk","Şahin","Yıldırım","Güven","Çimen","Ateş","Yaşar","Uzun","Yaman","Gürsoy"]
meslekler = ["Mühendis","Mimar","Bankacı","Memur","Operatör","Şoför","Esnaf","İşsiz"]

for x in range(1,10):
    df = df.append({
        "id":"10" + str(x),
        "isim": random.choice(isimler),
        "soyisim": random.choice(soyisimler),
        "yas": random.randint(18,65),
        "alacak": random.randint(500,5000),
        "verecek": random.randint(500,5000),
        "meslek": random.choice(meslekler)
    }, ignore_index=True)

df["alacak/verecek"] = df["alacak"] - df["verecek"]

#print(df[(df["alacak/verecek"]<0) & (df["meslek"] == "İşsiz")])

riskler = [
    (df["alacak/verecek"]<0) & (df["meslek"] == "İşsiz"),
    (df["alacak/verecek"]<0) & (df["yas"] >= 55),
    (df["alacak/verecek"]<0) & (df["yas"] < 55),
    (df["alacak/verecek"]>=0)
]
puanlama = ["A", "B", "C", "D"]

df["risk_grubu"] = np.select(riskler,puanlama)

print(df)