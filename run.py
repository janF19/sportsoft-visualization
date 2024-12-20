
from app import app
import threading
import subprocess
from waitress import serve
import os

# Environment configuration
IS_PRODUCTION = os.getenv('RUNNING_IN_PRODUCTION', 'false').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))
HOST = '0.0.0.0' if IS_PRODUCTION else 'localhost'

def run_streamlit():
    subprocess.run(['streamlit', 'run', 'streamlit_app.py'])

if __name__ == "__main__":
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    print(f"Starting Flask app on http://{HOST}:{PORT}")
    serve(app, host=HOST, port=PORT)