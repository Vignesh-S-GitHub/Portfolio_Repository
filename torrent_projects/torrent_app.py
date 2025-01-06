import asyncio
import os
from dotenv import load_dotenv
from aioseedrcc import Login, Seedr

# Load environment variables from .env file
load_dotenv()

# Access the variables
email = os.getenv('SEEDR_EMAIL')
password = os.getenv('SEEDR_PASSWORD')

# Read the token from a file
def read_token():
    try:
        with open('token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Token file not found. Please login to generate a token.")
        return None

# Write the token to a file
def write_token(token):
    with open('token.txt', 'w') as f:
        f.write(token)
    print("Token refreshed and updated.")

# Callback function to handle token refresh
async def after_refresh(seedr):
    write_token(seedr.token)

# Function to log in and retrieve a new token
async def login_and_save_token():
    async with Login(email, password) as seedr:
        response = await seedr.authorize()
        print("Login Response:", response)
        write_token(seedr.token)

# Function to add a magnet link
async def add_magnet_link():
    token = read_token()
    if not token:
        print("No valid token found. Please log in first.")
        return

    magnet_link = input("Enter the magnet link to add: ")

    async with Seedr(token=token, token_refresh_callback=after_refresh) as account:
        # Add the magnet link
        response = await account.add_torrent(magnet_link)
        print("Magnet Link Added:", response)

        # Optionally, list the contents of your Seedr account
        contents = await account.list_contents()
        print("Folder Contents:", contents)

        # Format the folder details
        formatted_folders = format_folder_data(contents)
        print(formatted_folders)

# Helper function to format bytes into human-readable format
def format_bytes(bytes_size):
    """
    Convert bytes into a human-readable format (e.g., MB, GB, TB).
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

# Function to format folder data into a human-readable form
def format_folder_data(folders):
    formatted_folders = []
    for folder in folders:
        size = format_bytes(folder['size'])
        last_update = folder['last_update']
        formatted_folders.append(f"""
        Folder Name: {folder['name']}
        Full Name: {folder['fullname']}
        Size: {size}
        Last Updated: {last_update}
        Shared: {'Yes' if folder['is_shared'] else 'No'}
        Play Audio: {'Yes' if folder['play_audio'] else 'No'}
        Play Video: {'Yes' if folder['play_video'] else 'No'}
        """)

    return "\n".join(formatted_folders)

# Function to check memory and bandwidth usage
async def check_usage():
    token = read_token()
    if not token:
        print("No valid token found. Please log in first.")
        return

    async with Seedr(token=token) as seedr:
        usage_data = await seedr.get_memory_bandwidth()

        def format_usage(data):
            """
            Format the usage data into a human-readable form.
            """
            bandwidth_used = format_bytes(data['bandwidth_used'])
            bandwidth_max = format_bytes(data['bandwidth_max'])
            space_used = format_bytes(data['space_used'])
            space_max = format_bytes(data['space_max'])

            return f"""
            Bandwidth Used: {bandwidth_used} of {bandwidth_max}
            Space Used: {space_used} of {space_max}
            Premium Status: {'Yes' if data['is_premium'] == 1 else 'No'}
            """

        # Output human-readable usage
        formatted_usage = format_usage(usage_data)
        print(formatted_usage)

# Function to delete files by item ID
async def delete_files():
    token = read_token()
    if not token:
        print("No valid token found. Please log in first.")
        return

    item_id = input("Enter the item ID to delete: ")
    item_type = input("Enter the item type (file/folder): ").lower()

    async with Seedr(token=token) as seedr:
        result = await seedr.delete_item(item_id, item_type)
        print(f"Delete Result: {result}")

# Main execution function
async def main():
    token = read_token()
    if not token:
        print("No token found. Logging in...")
        await login_and_save_token()
    else:
        print("Token found. Choose an action:")

    while True:
        print("\nOptions:")
        print("1. Add a magnet link")
        print("2. Check memory and bandwidth usage")
        print("3. Delete files")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            await add_magnet_link()
        elif choice == "2":
            await check_usage()
        elif choice == "3":
            await delete_files()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
