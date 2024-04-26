import json
import matplotlib.pyplot as plt
from collections import Counter
import os

# def extract_task_data(file_path):
    
#     folder_path = 'src'
    
#     #Check if the folder path exists
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

#     file_name = 'output_results.json'
#     file_path = f'{folder_path}/{file_name}' 


#     # Writing the JSON data to the file
#     with open(file_path, 'w') as file:
#         json.dump(tasks, file, indent=4)  # 'indent=4' for pretty-printing, remove if not necessary

#     print(f'JSON data has been written to {file_path}')

#     # Assuming you convert tasks to JSON and save them
#     with open('src/output_results.json', 'r') as file:
#         data = json.load(file) # Ensure this matches your JSON structure

#     # Extract tasks and categorize by status
#     projects = defaultdict(lambda: Counter({'To Do': 0, 'Doing': 0, 'Done': 0}))

#     # names = []
#     if 'results' in data:
#         for item in data['results']:
#             # Check if the 'properties' key and needed sub-keys are in each item
#             if 'properties' in item and 'Name' in item['properties'] and 'title' in item['properties']['Name']:
#                 # Extract the name of the page from the 'title' list (taking the first title entry's 'plain_text' if available)
#                 name = item['properties']['Name']['title'][0]['plain_text'] if item['properties']['Name']['title'] else 'No Name'
#                 status = item['properties']['Status']['select']['name'] if 'Status' in item['properties'] and 'select' in item['properties']['Status'] else 'Uncategorized'
                
#                 projects[name][status] += 1

                
#                 if name:
#                     # print("Type of name_info:", type(name_info))
#                     print("Content of name_info:", name)
#                 # if isinstance(name_info, list) and len(name_info) > 0:
#                 #     print("Type of name_info[0]:", type(name_info[0]))
#                 # if isinstance(name_info[0], dict):
#                 #     name = name_info[0].get('plain_text', 'No Name')
#                 else:
#                     print("Error: name_info[0] is not a dictionary")
#                     name = 'No Name'

                
#             else:
#                 print("Error: name_info is not a list or is empty")
#                 name = 'No Name'
        
#                 # Extract the status if available
#                 status = item['properties']['Status ']['select']['name'] if 'Status ' in item['properties'] and 'select' in item['properties']['Status '] else 'No Status'
#                 # Extract the creation date
#                 created_time = item['created_time'] if 'created_time' in item else 'No Creation Date'
#                 # Extract the URL of the page
#                 url = item['url'] if 'url' in item else 'No URL'

#                 # Print or process the information as needed
#                 print(f'Name: {name}, Status: {status}, Created on: {created_time}, URL: {url}')
#     else:
#         print('No results found in the JSON data.')

# def plot_title_frequencies(json_file):
#     # Load JSON data from a file
#     with open(json_file, 'r') as file:
#         data = json.load(file)

#     for item in data['results']:
#         print(type(item))
#         print(type(item['properties']))
#         print(type(item['properties']['Name']))
        
#         # Check if 'Name' and 'title' keys exist and 'title' is a list
#         if 'Name' in item['properties'] and 'title' in item['properties']['Name'] and isinstance(item['properties']['Name']['title'], list):
#             if item['properties']['Name']['title']:  # Check if the list is not empty
#                 title = item['properties']['Name']['title'][0]
#                 if 'plain_text' in title:  # Check if 'plain_text' key exists
#                     print(title['plain_text'])  # Print the plain_text for debugging
#                 else:
#                     print("No plain_text key found in title")
#             else:
#                 print("Title list is empty")
#         else:
#             print("Name or title key not found, or title is not a list")
        
#         try:
#             titles = [item['properties']['Name']['title'][0]['plain_text'] for item in data['results'] if 'Name' in item['properties'] and 'title' in item['properties']['Name'] and isinstance(item['properties']['Name']['title'], list) and item['properties']['Name']['title']]
#             print(titles)
#         except Exception as e:
#             print(f"An error occurred: {e}")
    
#     # Count the frequency of each title
#     title_counts = Counter(titles)

#     # Prepare data for plotting
#     labels, values = zip(*title_counts.items())

#     # Create bar chart
#     plt.figure(figsize=(10, 8))
#     plt.bar(labels, values, color='blue')
#     plt.xlabel('Titles')
#     plt.ylabel('Frequency')
#     plt.title('Frequency of Titles in JSON Data')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()

#     # Show the plot
#     plt.show()