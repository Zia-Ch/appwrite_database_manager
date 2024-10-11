from src.codebase_scanner import CodebaseScanner
from src.appwrite_api import AppwriteAPI

class ActionHandler:
    def __init__(self, config):
        self.scanner = CodebaseScanner()
        self.api = AppwriteAPI(config)

    def call_codebase_scaaner(self, cosebase_path):
        print("Scanning codebase...")
        classes = self.scanner.scan_codebase(root_dir=cosebase_path)
        print(f"Found {len(classes)} annotated classes.")
        existing_collections = self.api.list_collections()
        print(f"Found {len(existing_collections)} collections in the database.")

        for class_info in classes:
            if any(c['name'] == class_info['name'] for c in existing_collections):
                print(f"Collection '{class_info['name']}' already exists. Skipping it.")
                continue
            print(f"Creating collection '{class_info['name']}'...")
            self.api.create_collection(class_info)
            

    def call_file_scaaner(self, file_path):
        print(f"Scanning file: {file_path}...")
        class_info = self.scanner.scan_file(file_path)
        existing_collections = self.api.list_collections()
        print(f"Found {len(existing_collections)} collections in the database.")

        if any(c['name'] == class_info['name'] for c in existing_collections):
            print(f"Collection '{class_info['name']}' already exists. Skipping it.")
            return
        print(f"Creating collection '{class_info['name']}'...")
        self.api.create_collection(class_info)
        
