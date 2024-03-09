import argparse
import os
from telethon import TelegramClient, sync
from tqdm import tqdm
import asyncio

# Initial argparse configuration
parser = argparse.ArgumentParser(description='Download files from a Telegram channel.')
parser.add_argument('channel', help='Name or ID of the Telegram channel.')
parser.add_argument('directory', help='Directory where the files will be saved.')

# Parse command line arguments
args = parser.parse_args()

# Replace these values with your api_id and api_hash respectively
api_id = 'your_app_id_here'
api_hash = 'your_api_hash_here'

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def download_file(message, destination_path):
    with tqdm(total=message.file.size, unit='B', unit_scale=True, desc=message.file.name) as pbar:
        async def progress_callback(current_bytes, total_bytes):
            pbar.update(current_bytes - pbar.n)

        await message.download_media(file=destination_path, progress_callback=progress_callback)

async def main():
    files_needed_download = False  # Initially assume no files need to be downloaded

    # First, check if any files need to be downloaded or are incomplete
    async for message in client.iter_messages(args.channel):
        if message.file:
            destination_path = os.path.join(args.directory, message.file.name or "unnamed_file")
            if not os.path.exists(destination_path) or os.path.getsize(destination_path) < message.file.size:
                files_needed_download = True
                break  # Stop the check once we find a file that needs to be downloaded

    # Proceed with downloading if needed
    if files_needed_download:
        async for message in client.iter_messages(args.channel):
            if message.file:
                destination_path = os.path.join(args.directory, message.file.name)
                if os.path.exists(destination_path):
                    existing_size = os.path.getsize(destination_path)
                    if existing_size < message.file.size:
                        print(f"The file {message.file.name} is incomplete. Downloading again...")
                        os.remove(destination_path)
                    else:
                        print(f"The file {message.file.name} already exists and is complete. Skipping download.")
                        continue
                attempts = 3
                for i in range(attempts):
                    try:
                        print(f"Attempt {i+1} of {attempts} to download {message.file.name}")
                        await download_file(message, destination_path)
                        print(f"Successfully downloaded {message.file.name}.")
                        break  # Exit the loop if the download was successful
                    except (RpcError, asyncio.TimeoutError) as e:
                        print(f"Error downloading {message.file.name}: {e}")
                        if i < attempts - 1:
                            print("Retrying...")
                            await asyncio.sleep(2 ** i)  # Wait exponentially between retries
                        else:
                            print("Maximum attempts reached. Skipping file.")
    else:
        print("All files have already been downloaded and are complete.")

with client:
    client.loop.run_until_complete(main())