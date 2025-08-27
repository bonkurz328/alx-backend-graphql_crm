#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta
import json

def send_order_reminders():
    # GraphQL endpoint
    url = "http://localhost:8000/graphql"
    
    # Calculate date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # GraphQL query to find pending orders from the last 7 days
    query = """
    query {
        orders(filter: {orderDate_Gte: "%s", status: "pending"}) {
            edges {
                node {
                    id
                    orderDate
                    status
                    customer {
                        email
                    }
                }
            }
        }
    }
    """ % seven_days_ago
    
    try:
        # Send GraphQL request
        response = requests.post(url, json={'query': query})
        response.raise_for_status()
        
        data = response.json()
        
        # Check for errors in GraphQL response
        if 'errors' in data:
            error_message = f"[{datetime.now()}] GraphQL Error: {data['errors']}\n"
            with open('/tmp/order_reminders_log.txt', 'a') as log_file:
                log_file.write(error_message)
            print("Error processing order reminders. Check logs for details.")
            return
        
        # Process orders
        orders = data.get('data', {}).get('orders', {}).get('edges', [])
        
        if not orders:
            log_message = f"[{datetime.now()}] No pending orders found from the last 7 days.\n"
            with open('/tmp/order_reminders_log.txt', 'a') as log_file:
                log_file.write(log_message)
            print("No pending orders to remind.")
            return
        
        # Log each order
        log_message = f"[{datetime.now()}] Processing {len(orders)} order reminders:\n"
        for order_edge in orders:
            order = order_edge['node']
            order_id = order['id']
            customer_email = order['customer']['email']
            order_date = order['orderDate']
            
            log_message += f"  - Order ID: {order_id}, Customer Email: {customer_email}, Date: {order_date}\n"
        
        log_message += "\n"
        
        # Write to log file
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(log_message)
        
        print("Order reminders processed!")
        
    except requests.exceptions.RequestException as e:
        error_message = f"[{datetime.now()}] Request Error: {str(e)}\n"
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(error_message)
        print(f"Error connecting to GraphQL endpoint: {e}")
    except Exception as e:
        error_message = f"[{datetime.now()}] Unexpected Error: {str(e)}\n"
        with open('/tmp/order_reminders_log.txt', 'a') as log_file:
            log_file.write(error_message)
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    send_order_reminders()
