import os
import json
import logging
from tqdm import tqdm
from main import update_image_metadata, update_scene_metadata, delete_tag

# Setup logging
logging.basicConfig(
    filename="backup_restore.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def list_jsonl_files():
    """Lists all .jsonl files in the current directory."""
    files = [f for f in os.listdir() if f.endswith(".jsonl")]
    return files

def choose_file(files):
    """Prompts the user to choose a file from the list."""
    if not files:
        print("No .jsonl files found in the current directory.")
        return None

    print("Select a .jsonl file to process:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    while True:
        choice = input("Enter the number of the file: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(files):
                return files[choice - 1]
        print("Invalid selection. Please enter a valid number.")

def process_jsonl(file_path):
    """Processes the selected .jsonl file line by line with progress tracking."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
    total_lines = len(lines)
    processed_lines = 0

    # Initialize tqdm progress bar
    with tqdm(total=total_lines, desc=f"Processing {file_path}", unit="line") as pbar:
        for line in lines:
            try:
                data = json.loads(line)
                _type = data['_type']
                data.pop('_type')

                if _type == "image" or _type == "scene":
                    tag_ids = [tag['id'] for tag in data.get('tags', [])]
                    data["tag_ids"] = tag_ids
                    data.pop('tags', None)

                # Call appropriate methods based on _type
                if _type == "image":
                    update_image_metadata(data)
                    logger.info(f"Successfully processed image: {data['id']}")
                elif _type == "scene":
                    update_scene_metadata(data)
                    logger.info(f"Successfully processed scene: {data['id']}")
                elif _type == "tag":
                    delete_tag(data['id'])
                    logger.info(f"Successfully deleted tag: '{data['name']}' (ID: {data['id']})")
                else:
                    logger.warning(f"Unknown type '{_type}' in line: {line.strip()} - Skipping")

                processed_lines += 1
                pbar.update(1)

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON in line: {line.strip()} - {e}")
                pbar.set_postfix_str(f"Error at line {processed_lines + 1}")

            except Exception as e:
                logger.error(f"Unexpected error processing line {processed_lines + 1}: {e}")
                pbar.set_postfix_str(f"Error at line {processed_lines + 1}")

    logger.info(f"Finished processing {file_path}: {processed_lines}/{total_lines} lines processed.")

def main():
    files = list_jsonl_files()
    selected_file = choose_file(files)

    if selected_file:
        print(f"Processing file: {selected_file}")
        process_jsonl(selected_file)

if __name__ == "__main__":
    main()
