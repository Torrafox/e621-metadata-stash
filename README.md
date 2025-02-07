# e621 Metadata Updater for Stash

A Python program designed to update metadata for images and videos in [Stash](https://stashapp.cc) using data from the [e621.net](https://e621.net) database. This tool automatically processes your local gallery by comparing file MD5 checksums with the latest database dump from e621, generating metadata, and syncing it with your Stash instance.


## Features

- Matches files in a user-defined gallery directory by MD5 checksum to entries in the e621 database.
- Automatically creates a CSV file (`processed_files.csv`) with matched metadata.
- Updates metadata in Stash for matched files:
  - URL
  - Date
  - Details (description)
  - Tags (new tags are created if necessary).
- Displays real-time progress
- Logs all actions to `update_log.txt`.


## Requirements

- Python 3.8 or higher
- Internet connection
- Installed and running instance of [Stash](https://stashapp.cc)
- Stash API key


# Installation

## One-liner Installation Command:

For **Linux/macOS**:
```bash
git clone <repository-url> && cd <repository-directory> && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

For **Windows**:
```bash
git clone <repository-url> && cd <repository-directory> && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

<details>

<summary>

## Manual Steps (Optional):

</summary>

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - For **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - For **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

</details>

# Configuration
   Edit `config.json` in the project directory:
   ```json
   {
     "stash_url": "http://localhost:9999",
     "stash_api_key": "YOUR_API_KEY",
     "data_directory": "/path/to/your/e621/gallery"
   }
   ```
   - Replace `localhost:9999` with your server IP address and port if necessary.
   - Replace `YOUR_API_KEY` with your Stash API key.
   - Set `data_directory` to the directory containing your local e621 gallery of images and videos.


## Where do I find my API key?

1. Navigate to [http://localhost:9999/settings?tab=security](http://localhost:9999/settings?tab=security).
2. Generate a new API key (if you haven’t already) and copy it.
3. Paste the API key into the `config.json` file under the `"api_key"` field.

For more details, see the [Stash Docs](https://docs.stashapp.cc/in-app-manual/configuration/?h=api+key#api-key).


# Usage

1. **Run the Program**:
   ```bash
   python main.py
   ```

2. **What the Program Does**:
   - Downloads the latest metadata dump from [e621.net](https://e621.net/db_export/).
   - Matches local gallery files to e621 metadata based on MD5 checksums.
   - Generates a new CSV file with the matched metadata.
   - Updates the metadata for matched files in StashApp.

3. **Monitor Progress**:
   - The terminal displays a progress bar with real-time metrics.
   - A detailed log of all actions is saved to `update_log.txt`.


## Restore Backup

Before making any changes to your Stash instance, the current state of the image/scene/tag is saved to a backup file. If something goes wrong, you can restore your backup by running the `restore_backup.py` script. This will process a .jsonl backup file in the project root directory and restore the images, scenes, and tags accordingly. The script will log the progress and any errors. To run it, use the following command:

```bash
python restore_backup.py
```

# Troubleshooting

- **Missing Dependencies**: Ensure all dependencies from `requirements.txt` are installed.
- **Connection Errors**: Verify that StashApp is running and accessible at the URL specified in `config.json`.
- **Gallery Not Found**: Ensure the `data_directory` in `config.json` points to the correct folder.
- **Unsupported File Types**: Only files with extensions like `jpg`, `png`, `webm`, and `mp4` are processed.


## Limitations

- **Site-Specific**: This tool only works with metadata from [e621.net](https://e621.net) and cannot process files from other sites.
- **Large Files**: The e621 metadata dump is approximately 1.4 GB, so ensure you have sufficient disk space and a stable internet connection.


## License

This project is licensed under the MIT License.