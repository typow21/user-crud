#!/bin/bash

# Define the docker-compose file (adjust the path if needed)
COMPOSE_FILE="docker-compose.yml"

# Function to stop and remove containers
function docker_decompose() {
    echo "Stopping and removing containers..."
    docker-compose -f "$COMPOSE_FILE" down
}

# Function to build and start containers
function docker_compose() {
    echo "Building and starting containers..."
    docker-compose -f "$COMPOSE_FILE" up -d --build
}

# Function to start existing containers without rebuilding
function docker_start() {
    echo "Starting existing containers..."
    docker-compose -f "$COMPOSE_FILE" start
}

# Main script execution
echo "Starting Docker management script..."

# Check command line arguments for specific action
if [[ "$1" == "compose" ]]; then
    docker_decompose
    docker_compose
elif [[ "$1" == "start" ]]; then
    docker_start
else
    echo "Usage: $0 {compose|start}"
    exit 1
fi

echo "Docker containers have been managed successfully."