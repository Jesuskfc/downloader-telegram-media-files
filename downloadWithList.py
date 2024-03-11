import asyncio
from telethon import TelegramClient
import os

api_id = os.getenv('TELEGRAM_API_ID')  # Asegúrate de definir estas variables en tu entorno
api_hash = os.getenv('TELEGRAM_API_HASH')

client = TelegramClient('session', api_id, api_hash)

async def list_files(channel):
    async with client:
        all_files = []
        async for message in client.iter_messages(channel, limit=None):
            if message.file:
                file_name = message.file.name if message.file.name else f"unnamed_{message.id}.dat"
                all_files.append((message.id, file_name))
                print(f"{len(all_files)}. {file_name}")

        selections = input("Introduce los números de los archivos que deseas descargar, separados por comas (ej. 1,3,5): ")
        selected_indices = [int(index.strip()) - 1 for index in selections.split(',')]  # Convertir a índices

        for index in selected_indices:
            message_id, file_name = all_files[index]
            message = await client.get_messages(channel, ids=message_id)
            await message.download_media(file=os.path.join("descargas", file_name))
            print(f"Descargado: {file_name}")

if __name__ == "__main__":
    channel_name = input("Introduce el nombre del canal: ")
    asyncio.run(list_files(channel_name))
