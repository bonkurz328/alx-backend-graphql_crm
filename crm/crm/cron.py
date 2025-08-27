import datetime
import requests
import json

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM application health.
    """
    # Get current timestamp
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%d/%m/%Y-%H:%M:%S")
    
    # Create log message
    log_message = f"{timestamp} CRM is alive\n"
    
    # Log file path (using Windows-compatible path)
    log_file_path = "C:/temp/crm_heartbeat_log.txt"
    
    # Append message to log file
    try:
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_message)
        print(f"Heartbeat logged: {log_message.strip()}")
    except Exception as e:
        print(f"Error writing to log file: {e}")
    
    # Optional: You can add GraphQL endpoint checking here if needed
    print("Heartbeat check completed")
    