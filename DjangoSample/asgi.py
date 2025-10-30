import os
import django
import copy
from django.core.asgi import get_asgi_application
from DjangoSample.fastapi_app import app as fastapi_app

print("DEBUG: DjangoSample/asgi.py is being loaded!")  # Added very early debug print
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoSample.settings')
django.setup()
django_asgi_app = get_asgi_application()

# Global flag to indicate if startup is complete
_startup_complete = False

async def application(scope, receive, send):
    global _startup_complete

    if scope['type'] == 'lifespan':
        message = await receive()
        if message['type'] == 'lifespan.startup':
            print("ASGI Lifespan: Handling startup event.")
            _startup_complete = True
            await send({'type': 'lifespan.startup.complete'})
            print("ASGI Lifespan: Startup complete.")
        elif message['type'] == 'lifespan.shutdown':
            print("ASGI Lifespan: Handling shutdown event.")
            _startup_complete = False
            await send({'type': 'lifespan.shutdown.complete'})
            print("ASGI Lifespan: Shutdown complete.")
    elif scope['type'] == 'http':
        print(f"ASGI Router: Received path: {scope['path']}")
        if scope['path'].startswith('/api'):
            print("ASGI Router: Routing to FastAPI app.")
            
            # Create a copy of the scope for FastAPI to avoid modifying the original
            fastapi_scope = copy.copy(scope)
            
            # Adjust the path for FastAPI to correctly route
            fastapi_scope['path'] = fastapi_scope['path'][len('/api'):] 
            
            # Explicitly set root_path in the scope for FastAPI
            # This is crucial for static files (like Swagger UI assets) to be found
            fastapi_scope['root_path'] = '/api' 
            
            print(f"ASGI Router: FastAPI scope path: {fastapi_scope['path']}, root_path: {fastapi_scope['root_path']}")
            await fastapi_app(fastapi_scope, receive, send)
        else:
            print("ASGI Router: Routing to Django app.")
            await django_asgi_app(scope, receive, send)
    else:
        print(f"ASGI Router: Non-HTTP scope type: {scope['type']}. Passing to Django.")
        await django_asgi_app(scope, receive, send)
