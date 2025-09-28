#!/usr/bin/env python3
"""
Selenium script to connect to an already open Chrome browser.
If Chrome is not open, it will start a new Chrome instance and connect to it.

Requirements:
- selenium
- psutil (for checking if Chrome is running)

Usage:
    python connect_already_open_chrome.py
"""

import subprocess
import time
import psutil
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChromeConnector:
    def __init__(self, debug_port=9222, user_data_dir=None, profile_directory="Default"):
        # NOTE: always need to pass profile_directory="Default" to avoid creating a new profile
        # when connecting to an existing Chrome instance and call driver.get()
        self.debug_port = debug_port
        self.user_data_dir = user_data_dir or "/tmp/chrome_debug_profile"
        self.profile_directory = profile_directory
        self.driver = None
        
    def is_chrome_running_with_debug(self):
        """Check if Chrome is running with remote debugging enabled."""
        try:
            # Check if the debug port is accessible
            response = requests.get(f"http://localhost:{self.debug_port}/json", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def is_chrome_process_running(self):
        """Check if any Chrome process is running."""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'chrome' in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False
    
    def start_chrome_with_debug(self):
        """Start Chrome with remote debugging enabled."""
        print(f"Starting Chrome with remote debugging on port {self.debug_port}...")
        
        # Chrome command with debugging options
        chrome_args = [
            "google-chrome",  # or "chromium-browser" on some systems
            f"--remote-debugging-port={self.debug_port}",
            f"--user-data-dir={self.user_data_dir}",
            f"--profile-directory={self.profile_directory}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-default-apps"
        ]
        
        try:
            # Start Chrome in the background
            subprocess.Popen(chrome_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for Chrome to start and debug port to be available
            max_wait = 10
            for i in range(max_wait):
                if self.is_chrome_running_with_debug():
                    print("Chrome started successfully with remote debugging!")
                    return True
                time.sleep(1)
                print(f"Waiting for Chrome to start... ({i+1}/{max_wait})")
            
            print("Chrome failed to start with remote debugging within timeout")
            return False
            
        except Exception as e:
            print(f"Error starting Chrome: {e}")
            return False
    
    def connect_to_chrome(self):
        """Connect Selenium WebDriver to the running Chrome instance."""
        try:
            # Configure Chrome options to connect to existing instance
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")
            
            # Disable logging to reduce noise
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent")
            
            # Create WebDriver instance
            print("Connecting Selenium to Chrome...")
            self.driver = webdriver.Chrome(options=chrome_options)
            print("Successfully connected to Chrome!")
            return True
            
        except Exception as e:
            print(f"Error connecting to Chrome: {e}")
            return False
    
    def get_or_create_connection(self):
        """Main method to get connection to Chrome - either existing or new."""
        print("Checking for existing Chrome with remote debugging...")
        
        if self.is_chrome_running_with_debug():
            print("Found Chrome with remote debugging enabled!")
            if self.connect_to_chrome():
                return self.driver
        else:
            print("No Chrome with remote debugging found.")
            
            # Check if Chrome is running without debugging
            if self.is_chrome_process_running():
                print("Chrome is running but without remote debugging.")
                print("Automatically starting new Chrome instance with remote debugging...")
            else:
                print("No Chrome process found. Starting new Chrome instance with remote debugging...")
            
            # Start new Chrome instance with debugging
            if self.start_chrome_with_debug():
                if self.connect_to_chrome():
                    return self.driver
        
        print("Failed to establish connection to Chrome")
        return None
    
    def close(self):
        """Close the WebDriver connection."""
        if self.driver:
            try:
                self.driver.quit()
                print("WebDriver connection closed")
            except Exception as e:
                print(f"Error closing WebDriver: {e}")


def main():
    """Main function demonstrating the Chrome connection."""
    connector = ChromeConnector()
    
    try:
        # Get connection to Chrome
        driver = connector.get_or_create_connection()
        
        if not driver:
            print("Could not establish connection to Chrome. Exiting.")
            return
        
        # Example usage - navigate to a website
        print("\n=== Testing the connection ===")
        driver.get("https://www.google.com")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        
        # Example: Search for something
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys("Selenium WebDriver")
            search_box.submit()
            
            # Wait for results
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            print("Search completed successfully!")
            
        except Exception as e:
            print(f"Error during search test: {e}")
        
        # Keep the browser open for demonstration
        print("\nConnection established successfully!")
        print("The browser will remain open. Close it manually when done.")
        print("Press Ctrl+C to close the WebDriver connection...")
        
        # Keep the script running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
    
    finally:
        # Clean up
        connector.close()


if __name__ == "__main__":
    main()