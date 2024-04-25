# src/main.py

from src.api.client import NotionClient
from src.services.task_service import TaskService
from src.config.settings import API_KEY, DATABASE_ID
from src.utils.helpers import plot_title_frequencies
import json
import os
from collections import Counter
import matplotlib.pyplot as plt

def main():
    # Initialize the Notion client with configuration settings
    client = NotionClient(api_key=API_KEY, database_id=DATABASE_ID)
    
    # Initialize the service with the API client
    task_service = TaskService(client)
    
    # Example task operations
    tasks = task_service.fetch_all_tasks()
    
    
    folder_path = 'src'

    #Check if the folder path exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = 'output_results.json'
    file_path = f'{folder_path}/{file_name}' 


    # Writing the JSON data to the file
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)  # 'indent=4' for pretty-printing, remove if not necessary

    print(f'JSON data has been written to {file_path}')

    # Assuming you convert tasks to JSON and save them
    with open('src/output_results.json', 'r') as file:
        data = json.load(file) # Ensure this matches your JSON structure

    names = []
    if 'results' in data:
        for item in data['results']:
            # Check if the 'properties' key and needed sub-keys are in each item
            if 'properties' in item and 'Name' in item['properties'] and 'title' in item['properties']['Name']:
                # Extract the name of the page from the 'title' list (taking the first title entry's 'plain_text' if available)
                name_info = item['properties']['Name']['title'][0]['plain_text'] if item['properties']['Name']['title'] else 'No Name'
                names.append(name_info)

                if name_info:
                    # print("Type of name_info:", type(name_info))
                    print("Content of name_info:", name_info)
                # if isinstance(name_info, list) and len(name_info) > 0:
                #     print("Type of name_info[0]:", type(name_info[0]))
                # if isinstance(name_info[0], dict):
                #     name = name_info[0].get('plain_text', 'No Name')
                else:
                    print("Error: name_info[0] is not a dictionary")
                    name = 'No Name'

                
            else:
                print("Error: name_info is not a list or is empty")
                name = 'No Name'
        
                # Extract the status if available
                status = item['properties']['Status ']['select']['name'] if 'Status ' in item['properties'] and 'select' in item['properties']['Status '] else 'No Status'
                # Extract the creation date
                created_time = item['created_time'] if 'created_time' in item else 'No Creation Date'
                # Extract the URL of the page
                url = item['url'] if 'url' in item else 'No URL'

                # Print or process the information as needed
                print(f'Name: {name}, Status: {status}, Created on: {created_time}, URL: {url}')
    else:
        print('No results found in the JSON data.')
   
    


if __name__ == "__main__":
    main()
