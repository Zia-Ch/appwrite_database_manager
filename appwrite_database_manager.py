
from dotenv import load_dotenv
from src.action_handler import ActionHandler
from src.config import AppwriteConfig
from src.user_interface import UserInterface
from src.exceptions import AppwriteDatabaseManagerError

class AppwriteDatabaseManager:
    def __init__(self):
        load_dotenv()
        self.config = AppwriteConfig()
        self.ui = UserInterface()
        self.action_handler = ActionHandler(self.config)


    def run(self):
        try:
            # User interaction
            action = self.ui.get_user_action()
            if action == "1":
                create_mode = self.ui.get_create_mode()
                if create_mode == "1":
                    codebase_path = self.ui.get_codebase_path()
                    self.action_handler.call_codebase_scaaner(cosebase_path=codebase_path)
                elif create_mode == "2":
                    file_path = self.ui.get_file_path()
                    self.action_handler.call_file_scaaner(file_path)
            elif action == "2":
                print("Update mode is not implemented yet. It has some bugs.")
                # The update logic can go here in the future
            print("Operation completed successfully.")
        except AppwriteDatabaseManagerError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    app = AppwriteDatabaseManager()
    app.run()