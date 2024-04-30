# src/services/task_service.py

class TaskService:
    def __init__(self, client):
        self.client = client

    def fetch_all_tasks(self):
        # Utilize the client to fetch tasks from Notion
        data = self.client.query_database()

        # Fetch user information based on user IDs in the database
        user_ids = self.extract_user_ids(data)
        users = self.client.fetch_users(user_ids)

        # Map user IDs to user information
        user_map = {user['id']: user for user in users}

        # Add user information to each task
        for result in data.get('results', []):
            properties = result.get('properties', {})
            assigned_to = properties.get('Assigned to', {}).get('people', [])
            for person in assigned_to:
                person_id = person['id']
                person_info = user_map.get(person_id, {})
                person.update(person_info)

        return data  # You might want to parse this data into a more useful format

    def extract_user_ids(self, data):
        user_ids = set()
        for result in data.get('results', []):
            properties = result.get('properties', {})
            assigned_to = properties.get('Assigned to', {}).get('people', [])
            for person in assigned_to:
                user_ids.add(person['id'])
        return list(user_ids)