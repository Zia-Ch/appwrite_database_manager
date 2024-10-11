class UserInterface:
    def get_user_action(self):
        while True:
            action = input("Do you want to create or update collections? \n1. create\n2. update\nselect action: ").lower()
            if action in ['1', '2']:
                return action
            print("Invalid input. Please enter '1' or '2'.")

    def get_create_mode(self):
        while True:
            mode = input("Do you want to create all collections or a single collection?\n1. all\n2. single\nselect action: ").lower()
            if mode in ['1', '2']:
                return mode
            print("Invalid input. Please enter '1' or '2'.")
            
            
    def get_codebase_path(self):
        return input("Enter the path to the codebase/project (default is current dir): ")
    
    def get_file_path(self):
        return input("Enter the file path: ")

    
    def get_collection_id(self):
        return input("Enter the collection ID to update: ")