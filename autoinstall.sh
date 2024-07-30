#!/bin/bash

# Function to handle errors gracefully
handle_error() {
    echo "Error: $1"
    exit 1
}

# Change Termux repo
#termux-change-repo || handle_error "Failed to change Termux repo."

# Update and upgrade packages
pkg update && pkg upgrade -y || handle_error "Failed to update and upgrade packages."

# Install Python and wget
pkg install python rust -y || handle_error "Failed to install Python and wget."

# Download HamsterKombatBot
git clone https://github.com/semeer37/HamsterKombatBot.git || handle_error "Failed to clone HamsterKombatBot Github repo" 

# Change directory to HamsterKombatBot
cd HamsterKombatBot || handle_error "Failed to change directory to HamsterKombatBot."

# Set up virtual environment
python -m venv venv || handle_error "Failed to create virtual environment."
source venv/bin/activate || handle_error "Failed to activate virtual environment."

# Install requirements
pip install -r requirements.txt || handle_error "Failed to install requirements."

# Copy .env-example to .env
cp .env-example .env || handle_error "Failed to copy .env-example to .env."

# Prompt user for API ID and API Hash
read -p "Enter your API ID: " API_ID
read -p "Enter your API Hash: " API_HASH

# Set API ID and API Hash in .env file
sed -i "s/^API_ID=.*/API_ID=${API_ID}/" .env
sed -i "s/^API_HASH=.*/API_HASH=${API_HASH}/" .env

# Run the Python script to create sessions
python main.py -a 1 || handle_error "Failed to create sessions."

# Run the Python script to start automation
python main.py -a 2 || handle_error "Failed to start automation."

echo "Automation started successfully."
