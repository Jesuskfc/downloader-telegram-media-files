# Telegram Channel Downloader

## Description

This script allows you to download all files from a public Telegram channel. It's built using Python and makes use of the Telethon library to interact with the Telegram API, as well as tqdm for progress bar visualization during downloads.

## Installation

Before running this script, you'll need to install the required Python libraries. It's recommended to use a virtual environment.

```bash
# Clone the repository
git clone https://jesuskfc/downloader-telegram-media-files.git
cd downloader-telegram-media-files

# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Usage

- 1. Obtain your api_id and api_hash from https://my.telegram.org and replace the placeholders in the script.
- 2. Run the script from the command line, specifying the channel and the directory where you want to save the files.

```bash
python download.py <channel_name_or_id> <destination_directory>
