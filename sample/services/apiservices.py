from django.conf import settings

class ApiService:
    def __init__(self):
        # Use the API_KEY from Django settings
        self.api_key = settings.API_KEY

    def get_data(self):
        # In a real application, you would use self.api_key to make API calls
        return {"message": "Data from ApiService", "api_key_used": self.api_key}
