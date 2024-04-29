# src/main.py
from src.api.client import NotionClient
from src.services.task_service import TaskService
from src.config.settings import API_KEY, DATABASE_ID
import json
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import subprocess
import requests


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

    # Extract tasks and categorize by status
    projects = defaultdict(lambda: Counter({'To Do': 0, 'Doing': 0, 'Done': 0}))

    # names = []
    if 'results' in data:
        for item in data['results']:
            # Check if the 'properties' key and needed sub-keys are in each item
            if 'properties' in item and 'Name' in item['properties'] and 'title' in item['properties']['Name']:
                # Extract the name of the page from the 'title' list (taking the first title entry's 'plain_text' if available)
                name = item['properties']['Name']['title'][0]['plain_text'] if item['properties']['Name']['title'] else 'No Name'
                status = item['properties']['Status']['select']['name'] if 'Status' in item['properties'] and 'select' in item['properties']['Status'] else 'Uncategorized'
                
                projects[name][status] += 1

                
                if name:
                    # print("Type of name_info:", type(name_info))
                    print("Content of name_info:", name)
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

    #Count the frequencies of each name
    # name_frequencies = Counter(names)

    # names = list(name_frequencies.keys())
    # frequencies = list(name_frequencies.values())
    project_names = list(projects.keys())

    todo_counts = [projects[name]['To Do'] for name in project_names]
    doing_counts = [projects[name]['Doing'] for name in project_names]
    done_counts = [projects[name]['Done'] for name in project_names]

    # Setting the positions and width for the bars
    # Plotting the bars - using horizontal bar chart this time
    plt.figure(figsize=(10, 15))

    # Filter for projects with a certain minimum number of total tasks to reduce clutter
    min_tasks_threshold = 5  # Set this to a level that makes sense for your data
    filtered_projects = {name: counts for name, counts in projects.items() if sum(counts.values()) > min_tasks_threshold}

    x = range(len(project_names))
    width = 0.25

    # Plotting the bars
    plt.figure(figsize=(12, 6))
    plt.bar(x, todo_counts, width, label='To Do', color='red')
    plt.bar([p + width for p in x], doing_counts, width, label='Doing', color='yellow')
    plt.bar([p + width * 2 for p in x], done_counts, width, label='Done', color='green')

    plt.xlabel('Project Names')
    plt.ylabel('Count of Tasks')
    plt.title('Task Status by Project')
    plt.xticks([p + width for p in x], project_names, rotation=45, ha='right')
    plt.legend()

    plt.tight_layout()
    folder_path_for_the_pic = 'src/results'
    file_name='my_plot.png'

    # Ensure the directory exists
    if not os.path.exists(folder_path_for_the_pic):
        os.makedirs(folder_path_for_the_pic)
    
    # Full path to the file
    full_path = os.path.join(folder_path_for_the_pic, file_name)

    # Save the figure
    plt.savefig(full_path)
    # plt.show()

    plt.close()
    print("Plot saved as 'example_plot.png'.")

    # git_push('src/results/my_plot.png','Update a plot')

    # embed_image_in_notion(API_KEY,DATABASE_ID,)


def git_push(file_path, commit_message='Update plot'):
    """
    Pushes a file to a Git repository.
    """
    try:
        # Add file to Git
        subprocess.run(['git', 'add', file_path], check=True)
        # Commit the changes
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        # Push the commit
        subprocess.run(['git', 'push'], check=True)

        print("File pushed to GitHub successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def embed_image_in_notion(notion_api_key, database_id, image_url):
    """
    Embed an image in a Notion page using the Notion API.
    """
    url = 'https://api.notion.com/v1/pages'
    headers = {
        'Authorization': f'Bearer {notion_api_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-05-13'
    }
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": "Task Status Visualization"}}
                ]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {"url": image_url}
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Image successfully embedded in Notion.")
    else:
        print(f"Failed to embed image: {response.text}")


if __name__ == "__main__":
    main()
