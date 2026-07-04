import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pmc.ncbi.nlm.nih.gov/articles/PMC3961252/table/pone-0090297-t002/"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")

headers = [td.get_text(strip=True) for td in table.find("thead").find_all("td")]

rows = []
for tr in table.find("tbody").find_all("tr"):
    rows.append([td.get_text(strip=True) for td in tr.find_all("td")])

df = pd.DataFrame(rows, columns=headers)
print(df)