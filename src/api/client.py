import requests
import json

class NotionClient:
    def __init__(self, api_key, database_id):
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = 'https://api.notion.com/v1/' #Using the Notion API
        

    def query_database(self):
        url = f'{self.base_url}databases/{self.database_id}/query'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Notion-Version': '2022-02-22',
            'Content-Type':'application/json'
        }
        response = requests.post(url, headers=headers)
        return response.json()
    
    def fetch_users(self, user_ids):
        url = f'{self.base_url}users'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Notion-Version': '2022-02-22',
            'Content-Type': 'application/json'
        }
        params = {
            'user_ids': user_ids
        }
        response = requests.post(url, headers=headers, params=params)
        users = response.json().get('results', [])
        print(users)
        return users