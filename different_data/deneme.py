import numpy as np
import pandas as pd

df = pd.read_excel("tum_ykv_birlesim.xlsx")

list1 = df["Ekim"].values.tolist() + df["Aralık"].values.tolist()
#print(list1)

#cleanedList = [x for x in list1 if x != " nan"]

list_no_nan = [x for x in list1 if pd.notnull(x)]

print(list_no_nan)

"""
gecici_kume = set(list1)
tum_veriler_essiz = list(gecici_kume)

print(tum_veriler_essiz)
"""