#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def run_script(script_path):
    try:
        # Get the absolute path of the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        full_path = os.path.join(project_root, script_path)
        
        print(f"Executing: {full_path}")
        process = subprocess.Popen(['python3', full_path])
        return process
    except Exception as e:
        print(f"Error executing {script_path}: {str(e)}")
        sys.exit(1)

def main():
    # First run the server
    server_process = run_script('producto_libs/comm_servidor_mod.py')
    
    # Wait a moment to ensure server is up
    time.sleep(2)
    
    # Then run the client
    client_process = run_script('producto_libs/comm_cliente_mod.py')
    
    try:
        # Wait for both processes to complete
        server_process.wait()
        client_process.wait()
    except KeyboardInterrupt:
        print("\nStopping processes...")
        server_process.terminate()
        client_process.terminate()
        server_process.wait()
        client_process.wait()

if __name__ == "__main__":
    main() 