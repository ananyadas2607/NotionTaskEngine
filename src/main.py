# src/main.py

from src.api.client import NotionClient
from src.services.task_service import TaskService
from src.config.settings import API_KEY, DATABASE_ID

def main():
    # Initialize the Notion client with configuration settings
    client = NotionClient(api_key=API_KEY, database_id=DATABASE_ID)
    
    # Initialize the service with the API client
    task_service = TaskService(client)
    
    # Example task operations
    tasks = task_service.fetch_all_tasks()
    print(tasks)
    # for task in tasks:
    #     print(task)

if __name__ == "__main__":
    main()
