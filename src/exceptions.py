class AppwriteDatabaseManagerError(Exception):
    """Base exception for Appwrite Database Manager errors."""
    pass

class CodebaseScannerError(AppwriteDatabaseManagerError):
    """Exception raised for errors in the codebase scanning process."""
    pass

class AppwriteAPIError(AppwriteDatabaseManagerError):
    """Exception raised for errors in Appwrite API interactions."""
    pass

class ConfigurationError(AppwriteDatabaseManagerError):
    """Exception raised for errors in configuration settings."""
    pass

class UserInputError(AppwriteDatabaseManagerError):
    """Exception raised for invalid user inputs."""
    pass