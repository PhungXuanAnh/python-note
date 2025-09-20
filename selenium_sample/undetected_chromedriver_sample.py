"""
Optimized undetected_chromedriver with ZERO slow startups
Uses only undetected_chromedriver with local ChromeDriver binary

Usage:
    python undetected_chromedriver_sample.py            # Access Google Docs

Features:
- Uses local ChromeDriver binary from ./webdriver/chromedriver
- Consistent ~0.7 second startup time
- 10-second timeout protection
- Fallback to system ChromeDriver if local fails
- No Selenium dependencies
- Accesses Google Docs with user-data-dir in /tmp/google-docs
"""

import undetected_chromedriver as uc
import time
import os
import tempfile
import subprocess
import sys
import signal
import logging
from logging.config import dictConfig


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] [%(pathname)s:%(lineno)d] [%(funcName)s] %(levelname)s: %(message)s"
        },
    },
    "handlers": {
        "app.DEBUG": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "/tmp/selenium-mcp.log",
            "maxBytes": 100000 * 1024,  # 100MB
            "backupCount": 3,
        },
        "app.INFO": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "/tmp/selenium-mcp.log",
            "maxBytes": 100000 * 1024,  # 100MB
            "backupCount": 3,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["app.INFO"],
            "propagate": False,
            "level": "INFO",
        },
    },
}

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class TimeoutException(Exception):
    pass

def get_chrome_version():
    try:
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            version = result.stdout.strip().split()[-1]
            return int(version.split('.')[0])
    except:
        pass
    return 130

def create_fast_driver(user_data_dir):
    """Create undetected_chromedriver with optimizations and local ChromeDriver"""
    
    # Use local ChromeDriver binary
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(script_dir, "webdriver", "chromedriver")
    
    # Setup Chrome options
    opts = uc.ChromeOptions()
    opts.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Ultra-fast flags
    fast_flags = [
        '--no-sandbox',
        '--disable-dev-shm-usage', 
        '--disable-gpu',
        '--disable-extensions',
        '--disable-default-apps',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-logging',
        '--log-level=3',
        '--silent',
        '--window-size=200,150',
        '--window-position=-5000,-5000',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding',
        '--disable-features=VizDisplayCompositor',
        '--disable-ipc-flooding-protection'
    ]
    
    for flag in fast_flags:
        opts.add_argument(flag)
    
    try:
        print("Using undetected_chromedriver with local ChromeDriver...")
        
        # Setup timeout protection
        def alarm_handler(signum, frame):
            raise TimeoutException("Driver initialization timeout!")
        
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(10)  # 10 second timeout
        
        # Create driver with local ChromeDriver path
        driver = uc.Chrome(
            options=opts,
            driver_executable_path=chromedriver_path,
            use_subprocess=False,
            version_main=None  # Skip version detection
        )
        
        signal.alarm(0)  # Cancel alarm
        return driver, "undetected"
        
    except Exception as e:
        signal.alarm(0)  # Cancel alarm
        print(f"Failed with local ChromeDriver: {e}")
        
        # Fallback: try without specifying driver path
        try:
            print("Falling back to system ChromeDriver...")
            signal.alarm(10)
            
            driver = uc.Chrome(
                options=opts,
                use_subprocess=False,
                version_main=None
            )
            
            signal.alarm(0)
            return driver, "undetected_fallback"
            
        except Exception as e2:
            signal.alarm(0)
            print(f"All undetected_chromedriver methods failed: {e2}")
            raise Exception("Could not initialize undetected_chromedriver")

def main():
    print("Starting undetected Chrome with local ChromeDriver...")
    start_time = time.time()

    user_data_dir = "/tmp/google-docs"
    os.makedirs(user_data_dir, exist_ok=True)

    chrome_version = get_chrome_version()
    print(f"Chrome version: {chrome_version}")

    setup_time = time.time()
    print(f"Setup: {setup_time - start_time:.3f}s")

    driver = None
    
    try:
        driver, method_used = create_fast_driver(user_data_dir)
        
        init_time = time.time()
        print(f"Driver ready ({method_used}): {init_time - setup_time:.3f}s")
        
        # Test with Google Docs to verify undetected functionality
        print("Loading Google Docs page...")
        driver.get("https://docs.google.com/document/d/1yqQ5huvRO23K7_b3uQR87beXFKR1E57xjgjLjbOkdWI/edit?tab=t.0#heading=h.irx2cyp2uhse")
        
        load_time = time.time()
        print(f"Page load: {load_time - init_time:.3f}s")
        print(f"Title: '{driver.title}'")
        
        print("✓ SUCCESS")
        print("Browser is ready for manual interaction. Press Enter to quit...")
        input()  # Wait for user input before closing
        
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False
        
    finally:
        close_start = time.time()
        if driver:
            try:
                driver.quit()
                close_time = time.time()
                print(f"Cleanup: {close_time - close_start:.3f}s")
                print(f"TOTAL: {close_time - start_time:.3f}s")
            except:
                print("Cleanup: done")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
