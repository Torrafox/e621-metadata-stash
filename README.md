# e621 Metadata >>> Stash

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
git clone https://github.com/Torrafox/e621-metadata-stash.git && cd e621-metadata-stash && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

For **Windows**:
```bash
git clone https://github.com/Torrafox/e621-metadata-stash.git && cd e621-metadata-stash && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

<details>

<summary>

## Manual Steps (Optional):

</summary>

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Torrafox/e621-metadata-stash.git
   cd e621-metadata-stash
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


<details>

<summary>

### Example Output

</summary>

```console
[torrafox@file-island]$ git clone https://github.com/Torrafox/e621-metadata-stash.git && cd e621-metadata-stash && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
Cloning into 'e621-metadata-stash'...
remote: Enumerating objects: 17, done.
remote: Counting objects: 100% (17/17), done.
remote: Compressing objects: 100% (15/15), done.
remote: Total 17 (delta 5), reused 12 (delta 2), pack-reused 0 (from 0)
Receiving objects: 100% (17/17), 20.59 KiB | 1.58 MiB/s, done.
Resolving deltas: 100% (5/5), done.
Collecting git+https://github.com/Torrafox/e621-metadata-extractor.git (from -r requirements.txt (line 5))
  Cloning https://github.com/Torrafox/e621-metadata-extractor.git to /tmp/pip-req-build-jyeyl29i
  Running command git clone --filter=blob:none --quiet https://github.com/Torrafox/e621-metadata-extractor.git /tmp/pip-req-build-jyeyl29i
  Resolved https://github.com/Torrafox/e621-metadata-extractor.git to commit 6adea9de9e2c88cdb708df70da8cda1d6dfcbae5
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting requests (from -r requirements.txt (line 1))
  Using cached requests-2.32.3-py3-none-any.whl.metadata (4.6 kB)
Collecting beautifulsoup4 (from -r requirements.txt (line 2))
  Downloading beautifulsoup4-4.13.3-py3-none-any.whl.metadata (3.8 kB)
Collecting tqdm (from -r requirements.txt (line 3))
  Using cached tqdm-4.67.1-py3-none-any.whl.metadata (57 kB)
Collecting pandas (from -r requirements.txt (line 4))
  Using cached pandas-2.2.3-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (89 kB)
Collecting charset-normalizer<4,>=2 (from requests->-r requirements.txt (line 1))
  Using cached charset_normalizer-3.4.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (35 kB)
Collecting idna<4,>=2.5 (from requests->-r requirements.txt (line 1))
  Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting urllib3<3,>=1.21.1 (from requests->-r requirements.txt (line 1))
  Using cached urllib3-2.3.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests->-r requirements.txt (line 1))
  Using cached certifi-2025.1.31-py3-none-any.whl.metadata (2.5 kB)
Collecting soupsieve>1.2 (from beautifulsoup4->-r requirements.txt (line 2))
  Using cached soupsieve-2.6-py3-none-any.whl.metadata (4.6 kB)
Collecting typing-extensions>=4.0.0 (from beautifulsoup4->-r requirements.txt (line 2))
  Downloading typing_extensions-4.12.2-py3-none-any.whl.metadata (3.0 kB)
Collecting numpy>=1.26.0 (from pandas->-r requirements.txt (line 4))
  Using cached numpy-2.2.2-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (62 kB)
Collecting python-dateutil>=2.8.2 (from pandas->-r requirements.txt (line 4))
  Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)
Collecting pytz>=2020.1 (from pandas->-r requirements.txt (line 4))
  Using cached pytz-2025.1-py2.py3-none-any.whl.metadata (22 kB)
Collecting tzdata>=2022.7 (from pandas->-r requirements.txt (line 4))
  Using cached tzdata-2025.1-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting polars (from e621_metadata_extractor==0.1.1->-r requirements.txt (line 5))
  Downloading polars-1.22.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (14 kB)
Collecting pyarrow (from e621_metadata_extractor==0.1.1->-r requirements.txt (line 5))
  Using cached pyarrow-19.0.0-cp313-cp313-manylinux_2_28_x86_64.whl.metadata (3.3 kB)
Collecting oshash (from e621_metadata_extractor==0.1.1->-r requirements.txt (line 5))
  Using cached oshash-0.1.1-py3-none-any.whl
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas->-r requirements.txt (line 4))
  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Using cached requests-2.32.3-py3-none-any.whl (64 kB)
Downloading beautifulsoup4-4.13.3-py3-none-any.whl (186 kB)
Using cached tqdm-4.67.1-py3-none-any.whl (78 kB)
Using cached pandas-2.2.3-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.7 MB)
Using cached certifi-2025.1.31-py3-none-any.whl (166 kB)
Using cached charset_normalizer-3.4.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (144 kB)
Using cached idna-3.10-py3-none-any.whl (70 kB)
Using cached numpy-2.2.2-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.1 MB)
Using cached python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
Using cached pytz-2025.1-py2.py3-none-any.whl (507 kB)
Using cached soupsieve-2.6-py3-none-any.whl (36 kB)
Downloading typing_extensions-4.12.2-py3-none-any.whl (37 kB)
Using cached tzdata-2025.1-py2.py3-none-any.whl (346 kB)
Using cached urllib3-2.3.0-py3-none-any.whl (128 kB)
Downloading polars-1.22.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (32.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 32.9/32.9 MB 42.6 MB/s eta 0:00:00
Using cached pyarrow-19.0.0-cp313-cp313-manylinux_2_28_x86_64.whl (42.1 MB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Building wheels for collected packages: e621_metadata_extractor
  Building wheel for e621_metadata_extractor (pyproject.toml) ... done
  Created wheel for e621_metadata_extractor: filename=e621_metadata_extractor-0.1.1-py3-none-any.whl size=8240 sha256=39582c889db95063dd9a267e351d5b2b513917da445bbff825507c9707fe6ddd
  Stored in directory: /tmp/pip-ephem-wheel-cache-kt6k9yhg/wheels/ce/d0/8c/6c0b87160ae6ebe58487b6473d2d8cae7ca2fe89351557fdc6
Successfully built e621_metadata_extractor
Installing collected packages: pytz, urllib3, tzdata, typing-extensions, tqdm, soupsieve, six, pyarrow, polars, oshash, numpy, idna, charset-normalizer, certifi, requests, python-dateutil, beautifulsoup4, pandas, e621_metadata_extractor
Successfully installed beautifulsoup4-4.13.3 certifi-2025.1.31 charset-normalizer-3.4.1 e621_metadata_extractor-0.1.1 idna-3.10 numpy-2.2.2 oshash-0.1.1 pandas-2.2.3 polars-1.22.0 pyarrow-19.0.0 python-dateutil-2.9.0.post0 pytz-2025.1 requests-2.32.3 six-1.17.0 soupsieve-2.6 tqdm-4.67.1 typing-extensions-4.12.2 tzdata-2025.1 urllib3-2.3.0

(venv) [torrafox@file-island e621-metadata-stash]$ python main.py
Data directory validated: /home/torrafox/Pictures/e621
Fetching the latest database export URLs from e621...
Latest posts data export found: posts-2025-02-08.csv.gz
Latest tags data export found: tags-2025-02-08.csv.gz

Starting the download of the latest database dump...
Downloading: 100%|███████████████████████████████████████████████████████| 1.35G/1.35G [01:01<00:00, 23.7MB/s]
File downloaded successfully: posts-2025-02-08.csv.gz

Starting the download of the latest database dump...
Downloading: 100%|███████████████████████████████████████████████████████| 14.0M/14.0M [00:00<00:00, 59.9MB/s]
File downloaded successfully: tags-2025-02-08.csv.gz

Processing gallery directory and updating metadata...
Loading the CSV dump (this can take a minute)...
Scanning directory: /home/torrafox/Pictures/e621...
Processing files: 100%|████████████████████████████████████████████████████| 14/14 [00:00<00:00, 101.06file/s]

Writing results to e621_metadata.csv...
Processing complete! Results saved to e621_metadata.csv.
Total time elapsed: 0.14 seconds

Processing CSV file and updating metadata in Stash...
Processing files: 100%|█| 14/14 [00:02<00:00,  5.19file/s, updated=14, skipped=0, tags_created=333]
Processing complete.
Log saved to update_log_20250208123022.txt.
Backup saved to stash_backup_20250208123022.jsonl.
(venv) [torrafox@file-island e621-metadata-stash]$ 
```

</details>


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

This project is licensed under the [GPL-3.0 License](https://github.com/Torrafox/e621-metadata-stash?tab=readme-ov-file#GPL-3.0-1-ov-file).