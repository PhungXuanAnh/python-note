import subprocess
import os
from datetime import datetime
from pathlib import Path


def take_vm_screenshot(vm_name, output_dir="~/Downloads/vm-screenshot"):
    """
    Take a screenshot of a VirtualBox VM and save it with datetime filename.
    
    Args:
        vm_name (str): Name of the VM to take screenshot of
        output_dir (str): Directory to save the screenshot (default: ~/Downloads/vm-screenshot)
    
    Returns:
        str: Full filepath of the saved screenshot
    
    Raises:
        subprocess.CalledProcessError: If VBoxManage command fails
        FileNotFoundError: If VBoxManage is not found
    """
    # Expand user home directory and create output directory if it doesn't exist
    output_dir = os.path.expanduser(output_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with current datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    
    # Construct VBoxManage command
    cmd = ["VBoxManage", "controlvm", vm_name, "screenshotpng", filepath]
    
    try:
        # Execute the command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Verify the file was created
        if os.path.exists(filepath):
            print(f"Screenshot saved successfully: {filepath}")
            return filepath
        else:
            raise FileNotFoundError(f"Screenshot file was not created: {filepath}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error taking screenshot: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        raise
    except FileNotFoundError as e:
        print(f"VBoxManage command not found. Make sure VirtualBox is installed and in PATH.")
        raise


def main():
    """Example usage of the take_vm_screenshot function"""
    try:
        # Example: Take screenshot of ubuntu-22.04 VM
        vm_name = "ubuntu-22.04"
        screenshot_path = take_vm_screenshot(vm_name)
        print(f"Screenshot taken and saved to: {screenshot_path}")
        
    except Exception as e:
        print(f"Failed to take screenshot: {e}")


if __name__ == "__main__":
    main()
