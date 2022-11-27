import numpy as np
import pandas as pd

#excell verilerini dataframe'e dondurmek.
df = pd.read_excel("tum_ykv_birlesim.xlsx")

#0.satirdaki sutun basliklarini almak.
column_names = df.columns.values

#istedigimiz kolonun kacinci kolon olduguna bakmak icin.. (1 seferlik kullaniliyor)
"""
m = column_names
df_yeni = pd.DataFrame(m, columns=["var1"])
print(df_yeni)
"""

#0-39 , 42-48. sutunları tek bir listede toplama..
tum_veriler = []
for i in range(0,49):
    if(i == 40 or i == 41):
        continue
    tum_veriler += df[column_names[i]].values.tolist()

tum_veriler_bosluksuz = [x for x in tum_veriler if pd.notnull(x)]

#aynı verileri teke indirme (kumelerde bir deger en fazla bir kere olabilir)
gecici_kume = set(tum_veriler_bosluksuz)
tum_veriler_essiz = list(gecici_kume)

#40. sutun olan aradigimiz verileri bulma..
aradigimiz_veriler = []
aradigimiz_veriler += df[column_names[40]].values.tolist()

#aradigimiz verileri essiz yapma (non ve tekrar edenleri silme)
gecici_kume2 = set(aradigimiz_veriler)
aradigimiz_veriler_essiz = list(gecici_kume2)

#aradigimiz listede olup, tum verilerde olmayan verileri -> son_aranilan_listeye atama..
son_aranilan_liste = []
for i in range(0,len(aradigimiz_veriler_essiz)):
    if aradigimiz_veriler_essiz[i] not in tum_veriler_essiz:
        son_aranilan_liste.append(aradigimiz_veriler_essiz[i])


#son_aranilan_listeyi dataFrame'e cevirme
istenilen_df = pd.DataFrame(son_aranilan_liste, columns=["istenilen veriler"])
#dataFrame'i excel dosyasina cevirme..
istenilen_df.to_excel("essiz_veriler.xlsx")





