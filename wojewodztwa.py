# import requests
#
# API_URL = ('https://api-v3.mojepanstwo.pl/dane/powiaty.json?_type=objects&limit=500')
#
# lp = 1
#
# wojewodztwa = dict()
#
# def query_wojewodztwa_api():
#         data = requests.get(API_URL).json()
#         for i in range(0, 380):
#             w_id = data['Dataobject'][i]['data']['wojewodztwa.id']
#             w_nazwa = data['Dataobject'][i]['data']['wojewodztwa.nazwa']
#             print(w_id, '\t', w_nazwa)
#
#             if w_id not in wojewodztwa:
#                 wojewodztwa[w_id] = w_nazwa
#             else:
#                 print('exist')



wojewodztwa_list = {'5': 'Łódzkie', '3': 'Lubelskie', '12': 'Śląskie', '9': 'Podkarpackie', '2': 'Kujawsko-pomorskie', '15': 'Wielkopolskie', '11': 'Pomorskie', '6': 'Małopolskie', '7': 'Mazowieckie', '16': 'Zachodniopomorskie', '4': 'Lubuskie', '1': 'Dolnośląskie', '13': 'Świętokrzyskie', '8': 'Opolskie', '14': 'Warmińsko-mazurskie', '10': 'Podlaskie'}
