from .services.apiservices import ApiService

# Create a single instance of the service at module level
_api_service_instance = ApiService()

def get_api_service() -> ApiService:
    # Return the single instance
    return _api_service_instance
