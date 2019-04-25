import requests
from powiaty import powiaty_list
from wojewodztwa import wojewodztwa_list
from gminy import gminy_list
import pandas as pd
import time

import ray


start = time.time()

API_ALL_COPMAPNIES_URL = ('https://api-v3.mojepanstwo.pl/dane/krs_podmioty.json?_type=objects&page={}&limit={}')
API_CALL_COMPANY_URL = ('https://api-v3.mojepanstwo.pl/dane/krs_podmioty/{}.json')


comapanies_list = []

####################################################################################
# Download all companies id with name
####################################################################################

def query_all_companies_api(page, limit):
    data = requests.get(API_ALL_COPMAPNIES_URL.format(page, limit)).json()
    for i in range(0, limit):
        id = data['Dataobject'][i]['id']
        comapanies_list.append(id)

# query_all_companies_api(1, 50)


for i in range (1, 1379):
    query_all_companies_api(i, 500)


l1 = comapanies_list[:len(comapanies_list)//2]
l2 = comapanies_list[len(comapanies_list)//2:]


####################################################################################
# Download all company details - search by company_id from companies_list
####################################################################################

Companies = dict()

def call_company_api(company_id, dictionary):
    data = requests.get(API_CALL_COMPANY_URL.format(company_id)).json()
    name = data['data']['krs_podmioty.nazwa_skrocona']
    city = data['data']['krs_podmioty.adres_poczta']
    nip = data['data']['krs_podmioty.nip']
    community_id = data['data']['krs_podmioty.gmina_id']
    county_id = data['data']['krs_podmioty.powiat_id']
    voivodeship_id = data['data']['krs_podmioty.wojewodztwo_id']

    try:
        community = gminy_list[community_id]
        county = powiaty_list[county_id]
        voivodeship = wojewodztwa_list[voivodeship_id]

    except KeyError:
        community = community_id
        county = county_id
        voivodeship = voivodeship_id

    dictionary[name] = [city, county, community , voivodeship, nip]


ray.init()


@ray.remote
def call_l1_items():
    for k in l1:
        call_company_api(k, Companies)
    return Companies



@ray.remote
def call_l2_items():
    for k in l2:
        call_company_api(k, Companies)
    return Companies


ret_id1 = call_l1_items.remote()
ret_id2 = call_l2_items.remote()
ret1, ret2 = ray.get([ret_id1, ret_id2])


Companies = {**ret1, **ret2}

####################################################################################
# Creating pandas dataframe from dict Companies and export to csv
####################################################################################

def export_to_csv():
    df = pd.DataFrame.from_dict(Companies, orient="index", columns=["Miasto", "Powiat", "Gmina", "Województwo", "NIP" ])
    df.to_csv(r'export.csv', encoding='utf-8')


export_to_csv()

end = time.time()

print("Script was running %s" % (end - start))



