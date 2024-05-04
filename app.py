from flask import Flask, render_template
import json
import socket
import os
from collections import Counter, defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from src.api.client import NotionClient
from src.services.task_service import TaskService
from src.config.settings import API_KEY, DATABASE_ID

app = Flask(__name__)

from src.main import main as generate_plots

def fetch_and_save_tasks(client, file_path):
    task_service = TaskService(client)
    tasks = task_service.fetch_all_tasks()

    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)
    print(f'JSON data has been written to {file_path}')

def load_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def process_tasks(data):
    projects = defaultdict(lambda: Counter({'To Do': 0, 'Doing': 0, 'Done': 0}))
    assigned_to_list = defaultdict(lambda: defaultdict(int))
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

    return projects, assigned_to_list

def plot_task_data(projects, save_path):
    project_names = list(projects.keys())
    statuses = ['To Do', 'Doing', 'Done']
    status_counts = {status: [projects[name][status] for name in project_names] for status in statuses}
    
    plt.figure(figsize=(22, 10))
    x = range(len(project_names))
    width = 0.35
    for i, status in enumerate(statuses):
        plt.bar([p + width*i for p in x], status_counts[status], width, label=status)

    plt.xlabel('Project Names')
    plt.ylabel('Count of Tasks')
    plt.title('Task Status by Project')
    plt.xticks([p + width for p in x], project_names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    full_path = os.path.join(save_path, 'task_status_plot.png')
    plt.savefig(full_path)
    plt.close()
    print(f"Plot saved as '{full_path}'.")

@app.route('/')
def index():
    client = NotionClient(api_key=API_KEY, database_id=DATABASE_ID)
    file_path = 'src/output_results.json'
    save_path = 'src/static/results'
    
    fetch_and_save_tasks(client, file_path)
    data = load_data_from_file(file_path)
    projects, assigned_to_list = process_tasks(data)
    plot_task_data(projects, save_path)

    image_path = 'results/task_status_plot.png'
    return render_template('index.html', image_path=image_path)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to a free port provided by the host.
        return s.getsockname()[1]

if __name__ == '__main__':
    port = find_free_port()
    app.run(debug=True, port=port)

