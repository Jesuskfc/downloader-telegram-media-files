import argparse
import os
import asyncio
from telethon import TelegramClient
from tqdm import tqdm
import logging
from dotenv import load_dotenv

# Carga las variables de entorno desde .env
load_dotenv()

# Configura el logging
logging.basicConfig(filename='filtered_download_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initial argparse configuration
parser = argparse.ArgumentParser(description='Download files from a public Telegram channel that match given keywords.')
parser.add_argument('channel', help='Name or ID of the Telegram channel.')
parser.add_argument('directory', help='Directory where the files will be saved.')
parser.add_argument('keywords', nargs='+', help='Keywords to filter files by.')

# Parse command line arguments
args = parser.parse_args()

# Obtiene api_id y api_hash desde las variables de entorno
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# Verifica y crea el directorio de destino si no existe
if not os.path.exists(args.directory):
    os.makedirs(args.directory)
    logging.info(f"Created directory {args.directory}")

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def download_file(message, destination_path):
    try:
        with tqdm(total=message.file.size, unit='B', unit_scale=True, desc=message.file.name) as pbar:
            async def progress_callback(current_bytes, total_bytes):
                pbar.update(current_bytes - pbar.n)

            await message.download_media(file=destination_path, progress_callback=progress_callback)
        logging.info(f"Successfully downloaded {message.file.name}")
    except Exception as e:
        logging.error(f"Failed to download {message.file.name}: {e}")

async def main():
    try:
        async for message in client.iter_messages(args.channel, limit=None):
            if message.file:
                file_name = message.file.name if message.file.name else f"unnamed_{message.id}.dat"
                # Filtra los mensajes por las palabras clave proporcionadas
                if any(keyword.lower() in file_name.lower() for keyword in args.keywords):
                    destination_path = os.path.join(args.directory, file_name)
                    if not os.path.exists(destination_path) or os.path.getsize(destination_path) < message.file.size:
                        await download_file(message, destination_path)
                    else:
                        logging.info(f"File {file_name} already exists and is complete. Skipping download.")
                else:
                    logging.info(f"File {file_name} does not match keywords. Skipping download.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

with client:
    client.loop.run_until_complete(main())
