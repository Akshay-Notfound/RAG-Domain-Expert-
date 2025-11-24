import os
import sys

# Add the project root to sys.path so imports work as expected
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

# Import the FastAPI app
from src.rag_system.api.main import app as application

# Vercel looks for 'app'
app = application
