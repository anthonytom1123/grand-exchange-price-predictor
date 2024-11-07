import requests
import pandas as pd

# item codes https://www.runelocus.com/tools/osrs-item-id-list/
def request_data():
    item_list = list(range(554, 567)) #Runes
    data_dict = {}
    labels = ["timestamp"]
    
    for id in item_list:
        # historic daily prices
        # address = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json"
        get_historic_data(id, data_dict)
        get_catalogue_data(id, labels)
        
        print(labels)

def get_historic_data(id, data_dict):
    historic_address = f"https://secure.runescape.com/m=itemdb_oldschool/api/graph/{id}.json"
    historic_response = requests.get(historic_address)
    json_historic_data = historic_response.json()

    daily_dict = json_historic_data["daily"]
    for timestamp in daily_dict:
        if timestamp in data_dict:
            data_dict[timestamp].append(daily_dict[timestamp])
        else:
            data_dict[timestamp] = [daily_dict[timestamp]]

def get_catalogue_data(id, labels):
    catalogue_address = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json"
    catalogue_response = requests.get(catalogue_address, params={"item": id})
    labels.append(catalogue_response.json()["item"]["name"].lower().replace(" ", "_"))

def write_csv(data_dict, labels):
    return


request_data()