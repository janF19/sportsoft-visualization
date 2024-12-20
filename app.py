from flask import Flask, render_template, send_from_directory, redirect
import os
import pathlib
import pandas as pd
import subprocess
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get the absolute path to the sports_events directory
MAPS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.resolve(), 'static','sport_events')

# Get environment-specific configuration
IS_PRODUCTION = os.getenv('RUNNING_IN_PRODUCTION', 'false').lower() == 'true'
PORT = int(os.getenv('PORT', 10000))


# Set host based on environment
HOST = '0.0.0.0' if IS_PRODUCTION else 'localhost'
BASE_URL = os.getenv('RENDER_EXTERNAL_URL', f'http://{HOST}:{PORT}')
#STREAMLIT_URL = f'http://{HOST}:{STREAMLIT_PORT}'
#STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))

@app.route('/')
def index():
    try:
        map_files = [f for f in os.listdir(MAPS_DIRECTORY) if f.endswith('.html')]
    except FileNotFoundError:
        print(f"Directory not found: {MAPS_DIRECTORY}")
        map_files = []
    
    return render_template('index.html', map_files=map_files)

@app.route('/map/<filename>')
def display_map(filename):
    return send_from_directory(MAPS_DIRECTORY, filename)

@app.route('/charts')
def show_charts():
    # Start the Streamlit app in a separate thread when this route is accessed
    # streamlit_thread = threading.Thread(target=run_streamlit)
    # streamlit_thread.daemon = True
    # streamlit_thread.start()
    
    # return redirect(STREAMLIT_URL)
    
     # Start Streamlit as a subprocess
    streamlit_process = subprocess.Popen([
        'streamlit', 'run', 'streamlit_app.py',
        '--server.port', str(PORT),
        '--server.address', HOST,
        '--server.baseUrlPath', '/charts'
    ])
    
    return redirect(f"{BASE_URL}/charts")

def run_streamlit():
    print(f"Starting Streamlit app on {STREAMLIT_URL}")
    subprocess.run(['streamlit', 'run', 'streamlit_app.py', 
                   '--server.port', str(STREAMLIT_PORT),
                   '--server.address', HOST])

if __name__ == '__main__':
    
    
    os.makedirs(MAPS_DIRECTORY, exist_ok=True)
    print(app.url_map)
    app.run(host=HOST, port=PORT, debug=not IS_PRODUCTION)