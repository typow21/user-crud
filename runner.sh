#!/bin/bash

API_URL="http://localhost:8000"

print_menu() {
    echo "Select an action:"
    echo "1. View all users"
    echo "2. Get user by ID"
    echo "3. Delete user by ID"
    echo "4. Add a new user"
    echo "5. Exit"
}

get_users() {
    response=$(curl -s "${API_URL}/users")
    echo "$response" | jq . || echo "$response"  # Fallback to raw output if jq fails
}

get_user_by_id() {
    read -p "Enter user ID: " user_id
    response=$(curl -s "${API_URL}/user/${user_id}")
    echo "$response" | jq . || echo "$response"
}

delete_user_by_id() {
    read -p "Enter user ID to delete: " user_id
    response=$(curl -s -X DELETE "${API_URL}/user/${user_id}")
    echo "$response" | jq . || echo "$response"
}

add_user() {
    read -p "Enter first name: " first_name
    read -p "Enter middle name (optional): " middle_name
    read -p "Enter last name: " last_name
    read -p "Enter email address: " email_address
    read -p "Enter phone number: " phone_number

    user_data=$(jq -n --arg fn "$first_name" --arg mn "$middle_name" --arg ln "$last_name" --arg email "$email_address" --arg phone "$phone_number" \
        '{first_name: $fn, middle_name: $mn, last_name: $ln, email_address: $email, phone_number: $phone}')

    response=$(curl -s -X POST "${API_URL}/user" -H "Content-Type: application/json" -d "$user_data")
    echo "$response" | jq . || echo "$response"
}

while true; do
    print_menu
    read -p "Choose an option: " choice

    case $choice in
        1) get_users ;;
        2) get_user_by_id ;;
        3) delete_user_by_id ;;
        4) add_user ;;
        5) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid choice. Please try again." ;;
    esac
    echo ""
done