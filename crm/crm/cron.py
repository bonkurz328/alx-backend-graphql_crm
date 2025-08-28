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

def update_low_stock():
    """
    Cron job that runs every 12 hours to update low-stock products
    and logs the updates.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"\n{timestamp} - Starting low stock update\n"
    
    try:
        # Import and use the mutation directly instead of HTTP request
        from crm.schema import UpdateLowStockProducts
        from customers.models import Product
        
        # Get low stock products before update
        low_stock_before = Product.objects.filter(stock__lt=10)
        log_message += f"Found {low_stock_before.count()} low-stock products before update:\n"
        for product in low_stock_before:
            log_message += f"  - {product.name}: {product.stock}\n"
        
        # Execute the mutation directly
        result = UpdateLowStockProducts().mutate(None)
        
        # Log results
        log_message += f"\nMutation result: {result.message}\n"
        if result.products:
            log_message += "Updated products:\n"
            for product in result.products:
                log_message += f"  - {product.name}: Stock now {product.stock}\n"
        else:
            log_message += "No products were updated.\n"
            
    except Exception as e:
        log_message += f"Exception occurred: {str(e)}\n"
    
    # Append to log file (Windows compatible path)
    log_file_path = "C:/temp/low_stock_updates_log.txt"
    try:
        # Create directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_message)
        print(f"Low stock update logged successfully")
    except Exception as e:
        print(f"Error writing to log file: {e}")
