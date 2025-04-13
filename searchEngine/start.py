import pysolr
import subprocess
import requests
import time
import os

SOLR_PORT = '8983'
SOLR_CORE = 'mycore'
current_dir = os.path.dirname(os.path.abspath(__file__))
solr_bin = os.path.join(current_dir, "./solr-9.8.0/bin/solr.cmd") # Change this to your actual Solr directory path
# Function to start Solr if it's not already running
def start_solr():
    # Check if JAVA_HOME is set
    java_home = os.getenv("JAVA_HOME")
    if java_home:
        print(f"JAVA_HOME is set to: {java_home}")
    else:
        print("JAVA_HOME is not set. Please set it before proceeding.")
    
    # Start Solr in the background using subprocess.Popen (non-blocking)
    try:
        print("Starting Solr in the background...")
        process = subprocess.Popen([solr_bin, "start", "-p", "8983"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Solr started with PID: {process.pid}")

        # Wait a moment for Solr to initialize before proceeding with indexing
        time.sleep(15)  # You can adjust the wait time as needed
        print("To access Solr: http://localhost:8983/solr/")

        process.terminate()  # This stops the Solr subprocess

    except subprocess.CalledProcessError as e:
        print(f"Error starting Solr: {e}")
        print(e.output)
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")   

def stop_solr():
    # Check if JAVA_HOME is set
    java_home = os.getenv("JAVA_HOME")
    if java_home:
        print(f"JAVA_HOME is set to: {java_home}")
    else:
        print("JAVA_HOME is not set. Please set it before proceeding.") 
    
    # Start Solr in the background using subprocess.Popen (non-blocking)
    try:
        print("Stopping Solr in the background...")
        process = subprocess.Popen([solr_bin, "stop", "-p", "8983"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Solr stopped with PID: {process.pid}")

        # Wait a moment for Solr to initialize before proceeding with indexing
        time.sleep(5)  # You can adjust the wait time as needed
        print("To access Solr: http://localhost:8983/solr/")
        process.terminate()  # This stops the Solr subprocess
    except subprocess.CalledProcessError as e:
        print(f"Error starting Solr: {e}")
        print(e.output)
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}") 

def restart_solr():
    # Check if JAVA_HOME is set
    java_home = os.getenv("JAVA_HOME")
    if java_home:
        print(f"JAVA_HOME is set to: {java_home}")
    else:
        print("JAVA_HOME is not set. Please set it before proceeding.")
    
    # Start Solr in the background using subprocess.Popen (non-blocking)
    try:
        print("Restart Solr in the background...")
        process = subprocess.Popen([solr_bin, "restart", "-p", "8983"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait a moment for Solr to initialize before proceeding with indexing
        time.sleep(5)  # You can adjust the wait time as needed
        print("To access Solr: http://localhost:8983/solr/")
        process.terminate()  # This stops the Solr subprocess
    except subprocess.CalledProcessError as e:
        print(f"Error starting Solr: {e}")
        print(e.output)
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}") 

def create_core():
    """Create a core if it doesn’t exist."""
    # Check if the core exists
    response = requests.get(f"http://localhost:{SOLR_PORT}/solr/admin/cores?action=STATUS")
    
    if response.status_code == 200:
        cores = response.json().get('status', {})
        if SOLR_CORE in cores:
            print(f"Core '{SOLR_CORE}' already exists.")
        else:
            print(f"Core '{SOLR_CORE}' does not exist, creating it...")
            subprocess.run([solr_bin, "create", "-c", SOLR_CORE])
            print(f"Core '{SOLR_CORE}' created.")
    else:
        print(f"Failed to check core status. HTTP Status Code: {response.status_code}")


def delete_core():
    # Check if the core exists
    response = requests.get(f"http://localhost:{SOLR_PORT}/solr/admin/cores?action=STATUS")
    
    if response.status_code == 200:
        cores = response.json().get('status', {})
        if SOLR_CORE in cores:
            print(f"Core '{SOLR_CORE}' exist, deleting it...")
            subprocess.run([solr_bin, "delete", "-c", SOLR_CORE])
            print(f"Core '{SOLR_CORE}' deleted.")
        else:
            print(f"Core '{SOLR_CORE}' does not exist")
            
    else:
        print(f"Failed to check core status. HTTP Status Code: {response.status_code}")

start_solr()
#create_core()   
#delete_core()      
#stop_solr()
#restart_solr()

