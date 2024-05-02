# src/main.py
from src.api.client import NotionClient
from src.services.task_service import TaskService
from src.config.settings import API_KEY, DATABASE_ID
import json
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess
import requests
import streamlit as st
import pandas as pd


@st.cache(allow_output_mutation=True)
def fetch_and_process_data(api_key, database_id):
    client = NotionClient(api_key=api_key, database_id=database_id)
    task_service = TaskService(client)
    tasks = task_service.fetch_all_tasks()
    return tasks


def plot_data(data):
    project_names = list(data.keys())
    todo_counts = [data[name]['To Do'] for name in project_names]
    doing_counts = [data[name]['Doing'] for name in project_names]
    done_counts = [data[name]['Done'] for name in project_names]
    
    df = pd.DataFrame({
        'Project Names': project_names * 3,
        'Status': ['To Do'] * len(project_names) + ['Doing'] * len(project_names) + ['Done'] * len(project_names),
        'Count': todo_counts + doing_counts + done_counts
    })
    
    plt.figure(figsize=(16, 8))
    sns.barplot(x='Project Names', y='Count', hue='Status', data=df, palette=['red', 'yellow', 'green'])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return plt


def main():
    fetch_and_process_data(api_key=API_KEY, database_id=DATABASE_ID)
    
    folder_path = 'src'

    #Check if the folder path exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = 'output_results.json'
    file_path = f'{folder_path}/{file_name}' 


    # Writing the JSON data to the file
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)
        
    print(f'JSON data has been written to {file_path}')

    # Assuming you convert tasks to JSON and save them
    with open('src/output_results.json', 'r') as file:
        data = json.load(file) # Ensure this matches your JSON structure

    # Extract tasks and categorize by status
    projects = defaultdict(lambda: Counter({'To Do': 0, 'Doing': 0, 'Done': 0}))
    assigned_to_list = defaultdict(lambda: defaultdict(int))

    # names = []
    if 'results' in data:
        for item in data['results']:
            try:
                name = item['properties']['Name']['title'][0]['plain_text']
            except (KeyError, TypeError, IndexError):
                name = 'No Name'

            try:
                status = item['properties']['Status ']['select']['name']
            except (KeyError, TypeError):
                status = 'Uncategorized'

            try:
                assigned_to = item['properties']['Assigned to']['people'][0]['id']
            except (KeyError, TypeError, IndexError):
                assigned_to = 'Unassigned'

            projects[name][status] += 1
            assigned_to_list[name][assigned_to] += 1
    else:
        print('No results found in the JSON data.')

    # Printing assigned_to_list for debugging or analysis
    for name, assigned_to in assigned_to_list.items():
        print(f"Project: {name}")
        for assignee, count in assigned_to.items():
            print(f"Assigned to: {assignee}, Count: {count}")


    #Count the frequencies of each name
    # name_frequencies = Counter(names)

    # names = list(name_frequencies.keys())
    # frequencies = list(name_frequencies.values())
    project_names = list(projects.keys())
    print(project_names)
    todo_counts = [projects[name]['To Do'] for name in project_names]
    print(todo_counts)
    doing_counts = [projects[name]['Doing'] for name in project_names]
    print(doing_counts)
    done_counts = [projects[name]['Done \ud83d\ude4c'] for name in project_names]
    print(done_counts)
    nostatus_counts = [projects[name]['No Status'] for name in project_names]
    print(nostatus_counts)
    

    # Setting the positions and width for the bars
    # Plotting the bars - using horizontal bar chart this time
    plt.figure(figsize=(22, 10))
    x = range(len(project_names))
    width = 0.35

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

    if not os.path.exists(folder_path_for_the_pic):
        os.makedirs(folder_path_for_the_pic)
    full_path = os.path.join(folder_path_for_the_pic, 'my_plot.png')
    plt.savefig(full_path)
    plt.close()
    print(f"Plot saved as '{full_path}'.")

    sns.set_style("whitegrid")

    # Create a figure and axis
    plt.figure(figsize=(16, 8))

    
    df = pd.DataFrame({
        'Project Names': project_names * 3,
        'Status': ['To Do'] * len(project_names) + ['Doing'] * len(project_names) + ['Done'] * len(project_names),
        'Assigned To': ['Assigned To'] * len(project_names) * 3,
        'Count': todo_counts + doing_counts + done_counts
    })
    # Plot the data
    sns.barplot(x='Project Names', y='Count', hue='Status', data=df, palette=['red', 'yellow', 'green'])

    # Set the title and labels
    plt.xlabel('Project Names')
    plt.ylabel('Count of Tasks')
    plt.title('Task Status by Project')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Display the legend
    plt.legend(title='Status')

    # Show the plot
    plt.tight_layout()
    plt.show()
    folder_path_for_the_pic_2 = 'src/results/seaborn'

    if not os.path.exists(folder_path_for_the_pic_2):
        os.makedirs(folder_path_for_the_pic_2)
    full_path_1 = os.path.join(folder_path_for_the_pic_2, 'my_plot_2.png')
    plt.savefig(full_path_1)
    plt.close()
    print(f"Plot saved as '{full_path_1}'.")
    # url = 'https://example.com/upload'  # Replace with the upload URL provided by the tool
    # files = {'file': open('plot.png', 'rb')}  # Open the plot.png file in binary mode

    # response = requests.post(url, files=files)

    # if response.status_code == 200:
    #     print('Plot uploaded successfully.')
    # else:
    #     print('Failed to upload plot.')

    # Git and Notion integration functions can be called here as needed


    # git_push('src/results/my_plot.png','Update a plot')

    # embed_image_in_notion(API_KEY,DATABASE_ID,)

    st.title('Task Visualization Dashboard')
    api_key = st.sidebar.text_input("API_KEY")
    database_id = st.sidebar.text_input("DATABASE_ID")

    if st.sidebar.button('Fetch and Display Data'):
        if api_key and database_id:
            data = fetch_and_process_data(api_key, database_id)
            fig = plot_data(data)
            st.pyplot(fig)
        else:
            st.error("Please provide both API Key and Database ID")


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
