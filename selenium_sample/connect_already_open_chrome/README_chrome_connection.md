# Selenium Chrome Connection Scripts

This directory contains scripts to connect Selenium WebDriver to an already open Chrome browser, or automatically open a new Chrome instance if needed.

## Files

- `connect_already_open_chrome.py` - Main script with ChromeConnector class
- `simple_chrome_example.py` - Simple example showing how to use the connector
- `requirements_chrome_connect.txt` - Required Python packages

## Features

1. **Connect to existing Chrome**: If Chrome is running with remote debugging, connects to it
2. **Auto-start Chrome**: If no Chrome with debugging is found, starts a new instance
3. **Smart detection**: Checks if Chrome is running and provides helpful guidance
4. **Clean error handling**: Proper error handling and user feedback

## Installation

1. Install required packages:
```bash
pip install -r requirements_chrome_connect.txt
```

2. Make sure you have Chrome or Chromium installed:
```bash
# Ubuntu/Debian
sudo apt install google-chrome-stable
# or
sudo apt install chromium-browser

# For other systems, download from https://www.google.com/chrome/
```

## Usage

### Method 1: Use the main script
```bash
python connect_already_open_chrome.py
```

### Method 2: Use the simple example
```bash
python simple_chrome_example.py
```

### Method 3: Use in your own code
```python
from connect_already_open_chrome import ChromeConnector

connector = ChromeConnector()
driver = connector.get_or_create_connection()

if driver:
    driver.get("https://example.com")
    print(driver.title)
    # Your automation code here
    
    # Optional: close when done
    # connector.close()
```

## Manual Chrome Setup (Alternative)

If you prefer to start Chrome manually with remote debugging:

```bash
# Start Chrome with remote debugging
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_debug_profile
```

Then run the Python script to connect to it.

## Configuration Options

You can customize the ChromeConnector:

```python
# Custom debug port and user data directory
connector = ChromeConnector(
    debug_port=9223,  # Use different port
    user_data_dir="/path/to/custom/profile"
)
```

## How It Works

1. **Detection Phase**: 
   - Checks if Chrome is running with remote debugging on specified port
   - If not found, checks if any Chrome process is running

2. **Connection Phase**:
   - If debugging Chrome found: Connects directly
   - If regular Chrome found: Asks user permission to start new instance
   - If no Chrome found: Automatically starts new instance with debugging

3. **Selenium Connection**:
   - Uses Chrome's `--remote-debugging-port` feature
   - Connects Selenium WebDriver to the debugging port
   - Maintains connection until explicitly closed

## Troubleshooting

### Chrome won't start
- Make sure Chrome/Chromium is installed
- Check if the specified port (default 9222) is available
- Try a different port: `ChromeConnector(debug_port=9223)`

### Connection fails
- Ensure no firewall is blocking localhost connections
- Check if Chrome started with debugging: visit `http://localhost:9222` in browser
- Make sure Chrome didn't crash during startup

### Permission issues
- Chrome might need different user data directory
- Try: `ChromeConnector(user_data_dir="/tmp/my_chrome_profile")`

### Multiple Chrome instances
- The script will connect to the first Chrome instance with debugging
- To avoid conflicts, close other Chrome instances or use different profiles

## Notes

- The browser will remain open after the script ends (by design)
- Each script run reuses the same Chrome instance if it's still running
- Chrome profile is temporary by default (`/tmp/chrome_debug_profile`)
- For persistent sessions, specify a permanent `user_data_dir`