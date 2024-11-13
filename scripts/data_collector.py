import requests
import csv
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='logs/data_collector.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

# item codes https://www.runelocus.com/tools/osrs-item-id-list/
def collect_data():
    item_list = list(range(554, 567)) #Runes
    data_dict = {}
    labels = ["timestamp"]
    
    for id in item_list:
        request_historic_price_data(id, data_dict)
        request_item_catalogue_name_data(id, labels)
    
    write_to_csv(list(data_dict.values()), labels)
    logger.info("Finished collecting data.")

def request_historic_price_data(id, data_dict: dict):
    try:
        logger.info(f"Started collecting historical data for {id}.")
        historic_address = f"https://secure.runescape.com/m=itemdb_oldschool/api/graph/{id}.json"
        historic_response = requests.get(historic_address)
        json_historic_data = historic_response.json()

        daily_dict = json_historic_data["daily"]
        for timestamp in daily_dict:
            if timestamp in data_dict:
                data_dict[timestamp].append(daily_dict[timestamp])
            else:
                data_dict[timestamp] = [timestamp, daily_dict[timestamp]]
        logger.info(f"Finished collecting historic data for {id}.")
    except requests.exceptions.HTTPError as http_err: 
        logger.error(f"HTTP error occurred getting historic data for {id}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err: 
        logger.error(f"Connection error occurred getting historic data for {id}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err: 
        logger.error(f"Timeout error occurred getting historic data for {id}: {timeout_err}")
    except requests.exceptions.RequestException as req_err: 
        logger.error(f"An error occurred getting historic data for {id}: {req_err}")
    except Exception as e:
        logger.error(f"Error getting historic data for {id}: {e}")

def request_item_catalogue_name_data(id, labels):
    try:
        logger.info(f"Started collecting catalogue data for {id}.")
        catalogue_address = "https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json"
        catalogue_response = requests.get(catalogue_address, params={"item": id})
        labels.append(catalogue_response.json()["item"]["name"].lower().replace(" ", "_"))
        logger.info(f"Finished collecting catalogue data for {id}.")
    except requests.exceptions.HTTPError as http_err: 
        logger.error(f"HTTP error occurred getting catalogue data for {id}: {http_err}")
    except requests.exceptions.ConnectionError as conn_err: 
        logger.error(f"Connection error occurred getting catalogue data for {id}: {conn_err}")
    except requests.exceptions.Timeout as timeout_err: 
        logger.error(f"Timeout error occurred getting catalogue data for {id}: {timeout_err}")
    except requests.exceptions.RequestException as req_err: 
        logger.error(f"An error occurred getting catalogue data for {id}: {req_err}")
    except Exception as e:
        logger.error(f"Error getting catalogue data for {id}: {e}")

def write_to_csv(data: list, labels: list[str]):
    filename = "./data/raw/price_data.csv"
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(labels)
            writer.writerows(data)
    except Exception as e:
        logger.error(f"Error writing data csv: {e}")

collect_data()