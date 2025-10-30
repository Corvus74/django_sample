import uvicorn
import os
import sys
import django
from django.core.management import call_command

print("DEBUG: run_uvicorn.py started!")

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoSample.settings')
django.setup()

print("DEBUG: Django setup complete.")

# --- Run Django Migrations --- #
print("INFO: Applying database migrations...")
try:
    call_command('migrate')
    print("INFO: Database migrations applied successfully.")
except Exception as e:
    print(f"ERROR: Could not apply migrations: {e}")
    # Depending on the policy, you might want to exit here if migrations fail
    # sys.exit(1)

if __name__ == "__main__":
    # Now that migrations are applied, we can safely run Uvicorn
    uvicorn.run("DjangoSample.asgi:application", host="0.0.0.0", port=8000, reload=False)
