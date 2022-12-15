from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import pandas as pd

df = pd.read_excel("Royal Canin Youtube Büyüme Hesaplama.xlsx")

df[df.columns[8]] = df[df.columns[8]].fillna(0)

youtube_links = []
for i in range(0,len(df[df.columns[8]])):
    youtube_links.append(df[df.columns[8]][i])

channel_name = []
a = 0
for i in range(0,len(youtube_links)):
    try:
        url_input = youtube_links[i]
        url_opener = urlopen(Request(url_input, headers={'User-Agent': 'Mozilla'}))
        videoInfo = bs(url_opener, features="html.parser")

        video_title = videoInfo.title.get_text()

        channel_title = str(videoInfo.find("link", itemprop="name"))
        channel_name.append(channel_title[len('<link content="'):-len('" itemprop="name"/>')])
        print(f"{a}. kanal ismi alındı.")
        a += 1
    except:
        channel_name.append("N/A")

for i in range(0,len(youtube_links)):
    df[df.columns[9]][i] = channel_name[i]

df.to_excel("sonuc.xlsx")

