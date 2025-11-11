import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# Web scraping packages
from bs4 import BeautifulSoup as bs
import requests

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

r= requests.get('https://www.airbnb.com/s/Townsend--Tennessee--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&query=Townsend%2C%20TN&place_id=ChIJA-nECAilXogRuC_CJLjK3ao&date_picker_type=flexible_dates&checkin=2023-04-01&checkout=2023-04-30&adults=1&source=structured_search_input_header&search_type=autocomplete_click&federated_search_session_id=e9d8081c-7694-424c-88c0-6c030c687f3b&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MywiaXRlbXNfb2Zmc2V0Ijo3MiwidmVyc2lvbiI6MX0%3D')  

soup = bs(r.content,'html.parser')
# print(soup.get_text())


cabin_title = []

ab_cabin_title = soup.find_all('div', attrs = {'class' : 'nquyp1l s1cjsi4j dir dir-ltr'})


# Uncomment these two lines before the rest of the code to make it looks correct

for ab_cabin_title in ab_cabin_title:
   print(ab_cabin_title.text)