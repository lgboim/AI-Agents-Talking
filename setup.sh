#!/bin/bash

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found. Installing it..."
    pip install virtualenv
fi

# Create a virtual environment
echo "Creating virtual environment..."
virtualenv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the Streamlit app
echo "Starting the Streamlit app..."
streamlit run interactive_ai.py
