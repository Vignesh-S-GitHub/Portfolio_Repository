import asyncio
import streamlit as st
from aioseedrcc import Seedr
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read the Seedr token from .env
TOKEN = os.getenv("SEEDR_TOKEN")

# Utility functions for async operations
def run_async_function(coroutine):
    return asyncio.run(coroutine)

async def get_usage(seedr):
    return await seedr.get_memory_bandwidth()

async def list_files(seedr):
    return await seedr.list_contents()

async def add_magnet(seedr, magnet_link):
    return await seedr.add_torrent(magnet_link=magnet_link)

async def delete_item(seedr, item_id, item_type):
    return await seedr.delete_item(item_id=item_id, item_type=item_type)

async def scan_page(seedr, url):
    return await seedr.scan_page(url)

# Streamlit app
def main():
    st.title("Seedr Torrent Manager 🌟")
    st.sidebar.title("Navigation")
    options = ["Add Magnet Link", "View Usage", "Manage Files", "Scan Torrent Page"]
    choice = st.sidebar.selectbox("Choose an option:", options)

    if not TOKEN:
        st.error("Please set the SEEDR_TOKEN in your .env file.")
        return

    # Async context for Seedr
    async with Seedr(token=TOKEN) as seedr:
        if choice == "Add Magnet Link":
            st.subheader("Add a Magnet Link")
            magnet_link = st.text_input("Enter the Magnet Link:")
            if st.button("Add Torrent"):
                if magnet_link:
                    result = run_async_function(add_magnet(seedr, magnet_link))
                    st.success(f"Magnet link added: {result}")
                else:
                    st.warning("Please enter a valid magnet link.")

        elif choice == "View Usage":
            st.subheader("Memory & Bandwidth Usage")
            usage = run_async_function(get_usage(seedr))
            st.json(usage)

        elif choice == "Manage Files":
            st.subheader("Manage Files in Your Seedr Account")
            contents = run_async_function(list_files(seedr))
            if "folders" in contents or "files" in contents:
                if "folders" in contents:
                    st.write("Folders:")
                    for folder in contents["folders"]:
                        st.write(f"📁 {folder['name']} (ID: {folder['id']})")

                if "files" in contents:
                    st.write("Files:")
                    for file in contents["files"]:
                        st.write(f"📄 {file['name']} (ID: {file['id']})")
                        if st.button(f"Delete {file['name']}", key=f"delete_{file['id']}"):
                            run_async_function(delete_item(seedr, file["id"], "file"))
                            st.success(f"Deleted file: {file['name']}")
            else:
                st.info("No files or folders found.")

        elif choice == "Scan Torrent Page":
            st.subheader("Scan a Webpage for Torrents")
            url = st.text_input("Enter the URL to scan:")
            if st.button("Scan Page"):
                if url:
                    torrents = run_async_function(scan_page(seedr, url))
                    if torrents:
                        st.success("Torrents found:")
                        st.json(torrents)
                        for torrent in torrents.get("torrents", []):
                            st.write(f"📄 {torrent['name']} - {torrent['magnet_link']}")
                            if st.button(f"Add {torrent['name']}", key=f"add_{torrent['magnet_link']}"):
                                run_async_function(add_magnet(seedr, torrent["magnet_link"]))
                                st.success(f"Added torrent: {torrent['name']}")
                    else:
                        st.warning("No torrents found on this page.")
                else:
                    st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
