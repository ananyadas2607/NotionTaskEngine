import requests
import json

class NotionClient:
    def __init__(self, api_key, database_id):
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = 'https://api.notion.com/v1/'

    def query_database(self):
        url = f'{self.base_url}databases/{self.database_id}/query'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Notion-Version': '2022-02-22'
        }
        response = requests.post(url, headers=headers)
        return response.json()