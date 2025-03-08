#!/bin/bash

# Define script name and target directory
SCRIPT_NAME="dpy.py"
TARGET_DIR="/usr/local/bin"  # Preferred directory for user-installed executables

# Ensure the script exists
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Error: $SCRIPT_NAME not found!"
    exit 1
fi

# Copy script to /usr/local/bin
sudo cp "$SCRIPT_NAME" "$TARGET_DIR/"

# Rename to remove .py extension (optional)
sudo mv "$TARGET_DIR/$SCRIPT_NAME" "$TARGET_DIR/dpy"

# Make executable
sudo chmod +x "$TARGET_DIR/dpy"

# Verify installation
if command -v dpy &> /dev/null; then
    echo "Installation successful!"
else
    echo "Installation failed!"
fi
