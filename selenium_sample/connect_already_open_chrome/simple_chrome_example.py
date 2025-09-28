#!/usr/bin/env python3
"""
Simple example showing how to use the ChromeConnector class.
"""

from connect_already_open_chrome import ChromeConnector
import time


def simple_example():
    """Simple example of using ChromeConnector."""
    connector = ChromeConnector()
    
    try:
        # Get connection to Chrome
        driver = connector.get_or_create_connection()
        
        if not driver:
            print("Could not connect to Chrome")
            return
        
        print("Successfully connected! Opening example websites...")
        
        # Visit multiple websites
        websites = [
            "https://www.google.com",
            "https://www.github.com",
            "https://stackoverflow.com",
            "https://gemini.google.com/app"
        ]
        
        for site in websites:
            print(f"Navigating to {site}")
            driver.get(site)
            print(f"Title: {driver.title}")
            time.sleep(2)  # Wait a bit between navigations
        
        print("Demo completed! Browser will stay open.")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Note: We're not closing the driver to keep the browser open
        # Uncomment the next line if you want to close the browser
        # connector.close()
        pass


if __name__ == "__main__":
    simple_example()