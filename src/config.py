import os
from dataclasses import dataclass

@dataclass
class AppwriteConfig:
    api_endpoint: str
    project_id: str
    database_id: str
    api_key: str

    def __init__(self):
        self.api_endpoint = os.getenv('API_ENDPOINT')
        self.project_id = os.getenv('PROJECT_ID')
        self.database_id = os.getenv('DATABASE_ID')
        self.api_key = os.getenv('API_KEY')

        if not all([self.api_endpoint, self.project_id, self.database_id, self.api_key]):
            raise ValueError("Missing required environment variables")