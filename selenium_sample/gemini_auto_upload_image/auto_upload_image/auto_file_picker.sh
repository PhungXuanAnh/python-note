#!/bin/bash

# Automated file picker interaction script
# This script waits for a file dialog to appear and automatically selects the image file
# Usage: ./auto_file_picker.sh <file_path>

# Get file path from command line argument
FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    echo "Error: No file path provided"
    echo "Usage: $0 <file_path>"
    exit 1
fi

# Extract directory and filename from the file path
FILE_DIR=$(dirname "$FILE_PATH")
FILE_NAME=$(basename "$FILE_PATH")

echo "File path: $FILE_PATH"
echo "File directory: $FILE_DIR"
echo "File name: $FILE_NAME"

# Enable debug mode
set -x

echo "Starting automated file picker interaction..."
echo "DEBUG: Current user: $(whoami)"
echo "DEBUG: Current display: $DISPLAY"
echo "DEBUG: Current working directory: $(pwd)"
echo "DEBUG: Environment variables:"
env | grep -E "(DISPLAY|XAUTH|HOME|USER)" | sort
echo "DEBUG: Available X windows:"
xwininfo -root -tree 2>/dev/null | head -20 || echo "DEBUG: xwininfo failed"

# Function to handle file picker
handle_file_picker() {
    local max_attempts=10
    local attempt=0
    
    echo "DEBUG: Starting file picker handler with max_attempts=$max_attempts"
    
    while [ $attempt -lt $max_attempts ]; do
        echo "Attempt $((attempt + 1)): Looking for file picker dialog..."
        
        # List all windows before searching
        echo "DEBUG: All available windows:"
        xdotool search --name ".*" 2>/dev/null | while read window_id; do
            window_name=$(xdotool getwindowname "$window_id" 2>/dev/null || echo "Unknown")
            echo "  Window ID: $window_id, Name: $window_name"
        done
        
        # Search specifically for "Open Files" dialog title
        echo "DEBUG: Searching for 'Open Files' dialog..."
        DIALOG_ID=$(xdotool search --name "Open Files" 2>/dev/null | head -1)
        echo "DEBUG: Open Files dialog search result: '$DIALOG_ID'"
        
        if [ -n "$DIALOG_ID" ]; then
            echo "Found file dialog with ID: $DIALOG_ID"
            
            # Get window information
            window_name=$(xdotool getwindowname "$DIALOG_ID" 2>/dev/null || echo "Unknown")
            echo "DEBUG: Window name: $window_name"
            
            # Check if window is visible
            window_info=$(xwininfo -id "$DIALOG_ID" 2>/dev/null || echo "Failed to get window info")
            echo "DEBUG: Window info: $window_info"
            
            # Focus on the dialog
            echo "DEBUG: Attempting to focus window $DIALOG_ID"
            xdotool windowfocus $DIALOG_ID
            focus_result=$?
            echo "DEBUG: Focus result: $focus_result"
            sleep 0.5
            
            # Check current focused window
            current_focus=$(xdotool getwindowfocus 2>/dev/null || echo "Unknown")
            echo "DEBUG: Current focused window: $current_focus"
            
            # Navigate to the file location by typing the path
            echo "Typing file path..."
            echo "DEBUG: Sending Ctrl+L to window $DIALOG_ID"
            xdotool key --window $DIALOG_ID ctrl+l
            key_result=$?
            echo "DEBUG: Ctrl+L result: $key_result"
            sleep 0.5
            
            echo "DEBUG: Typing path '$FILE_DIR/'"
            xdotool type --window $DIALOG_ID "$FILE_DIR/"
            type_result=$?
            echo "DEBUG: Type path result: $type_result"
            
            echo "DEBUG: Sending Return key"
            xdotool key --window $DIALOG_ID Return
            return_result=$?
            echo "DEBUG: Return key result: $return_result"
            sleep 0.5

            # Select the image file
            echo "Selecting $FILE_NAME..."
            echo "DEBUG: Typing filename '$FILE_NAME'"
            xdotool type --window $DIALOG_ID "$FILE_NAME"
            filename_result=$?
            echo "DEBUG: Filename type result: $filename_result"
            sleep 0.5

            # Press Enter or click Open button
            echo "DEBUG: Sending final Return key"
            xdotool key --window $DIALOG_ID Return
            final_return_result=$?
            echo "DEBUG: Final Return result: $final_return_result"
            
            echo "File selection completed!"
            echo "DEBUG: All operations completed successfully"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo "DEBUG: No dialog found in attempt $attempt, waiting 0.5 seconds..."
        sleep 0.5
    done
    
    echo "File picker dialog not found after $max_attempts attempts"
    echo "DEBUG: Final failure - no dialog found"
    echo "DEBUG: Listing final window state:"
    xdotool search --name ".*" 2>/dev/null | head -10 | while read window_id; do
        window_name=$(xdotool getwindowname "$window_id" 2>/dev/null || echo "Unknown")
        echo "  Final Window ID: $window_id, Name: $window_name"
    done
    return 1
}

# Run the file picker handler
handle_file_picker

echo "Automated file picker script done"