# src/services/task_service.py

class TaskService:
    def __init__(self, client):
        self.client = client

    def fetch_all_tasks(self):
        # Utilize the client to fetch tasks from Notion
        data = self.client.query_database()
        # print(data)
        return data  # You might want to parse this data into a more useful format
