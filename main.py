import os
import sys
import json
import requests
import pandas as pd
from tqdm import tqdm
from collections import OrderedDict
from e621_metadata_extractor.fetcher import get_latest_dump_urls, download_file
from e621_metadata_extractor.extractor import process_directory

# Load configuration
def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as config_file:
        return json.load(config_file)
    
CONFIG = load_config()
backup_file = ""
log_file = ""

# GraphQL request function
def graphql_request(query, variables=None):
    """
    Send a GraphQL request to the Stash API.
    """
    headers = {
        "ApiKey": f"{CONFIG['stash_api_key']}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{CONFIG['stash_url']}/graphql", json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()

# Find image by checksum
def find_image(checksum):
    query = """
    query FindImage($checksum: String!) {
      findImage(checksum: $checksum) {
        id, date, details, photographer, tags {id, name}, urls
      }
    }
    """
    variables = {"checksum": checksum}
    data = graphql_request(query, variables)
    return data.get("data", {}).get("findImage")

# Find scene by checksum
def find_scene(oshash, checksum):
    query = """
    query FindScene($oshash: String, $checksum: String!) {
      findSceneByHash(input: { oshash: $oshash, checksum: $checksum }) {
        id, date, details, director, tags {id, name}, urls
      }
    }
    """
    variables = {"oshash": oshash, "checksum": checksum}
    data = graphql_request(query, variables)
    return data.get("data", {}).get("findSceneByHash")

# Query to retrieve all tags
def get_all_tags():
    """
    Fetch all tags from StashApp using the findTags query with per_page = -1 to retrieve all results.
    Returns a dictionary mapping tag names to their IDs.
    """
    query = """
    query FindTags {
      findTags(filter: {per_page: -1}) {
        tags {
          id
          name
        }
      }
    }
    """
    response = graphql_request(query)
    tags = response.get("data", {}).get("findTags", {}).get("tags", [])
    return {tag['name']: tag['id'] for tag in tags}  # Return a dictionary {name: id}

def process_tags(tag_string):
    """
    Ensure all tags in tag_string exist and return their corresponding IDs.
    """
    tag_names = tag_string.split()  # Split tag_string into individual tags
    existing_tags = get_all_tags()  # Retrieve all existing tags
    tag_ids = []  # List to store tag IDs
    log = []

    for tag_name in tag_names:
        if tag_name in existing_tags:
            tag_ids.append(existing_tags[tag_name])  # Use existing tag ID
            log.append(f"Tag '{tag_name}' already exists with ID {existing_tags[tag_name]}.")
        else:
            # Create a new tag
            new_tag = create_tag(tag_name)
            if new_tag:
                write_to_backup_file(new_tag, "tag", backup_file)
                existing_tags[tag_name] = new_tag['id']  # Update local cache
                tag_ids.append(new_tag['id'])  # Add new tag ID
                log.append(f"Tag '{tag_name}' created with ID {new_tag['id']}.")
            else:
                log.append(f"Failed to create tag '{tag_name}'.")
    
    return tag_ids, log

# Mutation to create a new tag
def create_tag(tag_name):
    mutation = """
    mutation CreateTag($input: TagCreateInput!) {
      tagCreate(input: $input) {
        id
        name
      }
    }
    """
    variables = {"input": {"name": tag_name}}
    response = graphql_request(mutation, variables)
    return response.get("data", {}).get("tagCreate")

# Mutation to delete a tag
def delete_tag(tag_id):
    mutation = """
    mutation DeleteTag($input: TagDestroyInput!) {
      tagDestroy(input: $input)
    }
    """
    variables = {"input": {"id": tag_id}}
    response = graphql_request(mutation, variables)
    return response.get("data", {}).get("tagDestroy")

# Update image metadata
def update_image_metadata(metadata):
    mutation = """
    mutation UpdateImage($input: ImageUpdateInput!) {
      imageUpdate(input: $input) {
        id
      }
    }
    """
    variables = {"input": {**metadata}}
    data = graphql_request(mutation, variables)
    return data.get("data", {}).get("imageUpdate")

# Update scene metadata
def update_scene_metadata(metadata):
    mutation = """
    mutation UpdateScene($input: SceneUpdateInput!) {
      sceneUpdate(input: $input) {
        id
      }
    }
    """
    variables = {"input": {**metadata}}
    data = graphql_request(mutation, variables)
    return data.get("data", {}).get("sceneUpdate")

def write_to_backup_file(json_data, type, file_name):
    if type == "image":
        json_data["_type"] = "image"
    elif type == "scene":
        json_data["_type"] = "scene"
    elif type == "tag":
        json_data["_type"] = "tag"

    with open(file_name, "a") as backup_file:
        backup_file.write(json.dumps(json_data) + "\n")

# Process the CSV file and update metadata
def process_csv_and_update_metadata(csv_file):
    """
    Process the CSV file and update metadata in StashApp, including tags.
    Display real-time progress in the terminal.
    """
    global backup_file
    global log_file

    now = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
    backup_file = f"stash_backup_{now}.jsonl"
    log_file = f"update_log_{now}.txt"

    df = pd.read_csv(csv_file)
    total_files = len(df)

    # Load configuration
    overwrite = CONFIG.get("overwrite_existing_metadata")
    import_artist = CONFIG.get("import_artist")
    import_date = CONFIG.get("import_creation_date")
    import_details = CONFIG.get("import_description")
    import_tags = CONFIG.get("import_tags")
    import_url = CONFIG.get("import_url")
    
    # Initialize progress tracking
    updated_count = 0
    skipped_files_count = 0
    created_tags_count = 0
    skipped_tags_count = 0    
    log = []

    # Use tqdm for progress bar
    with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
        for _, row in df.iterrows():
            checksum = str(row['md5']) if not pd.isna(row['md5']) else ""
            oshash = str(row['oshash']) if not pd.isna(row['oshash']) else ""
            file_ext = row['file_ext']

            # Find image or scene
            if file_ext in ["jpg", "jpeg", "png", "apng", "gif", "webp"]:
                entity = find_image(checksum)
                entity_type = "Image"
            elif file_ext in ["mp4", "webm", "mkv"]:
                entity = find_scene(oshash, checksum)
                entity_type = "Scene"
            else:
                skipped_files_count += 1
                log.append(f"File {checksum}: Skipped (unsupported file type \"{file_ext}\").")
                pbar.update(1)
                pbar.set_postfix(OrderedDict([
                    ("updated", updated_count),
                    ("skipped", skipped_files_count),
                    ("tags_created", created_tags_count),
                    ("tags_skipped", skipped_tags_count)
                ]))
                continue

            if entity:
                metadata = {}
                metadata["id"] = entity["id"]

                if import_artist:
                    # Get single artist from artist_string
                    artist = row["artist_string"].split(" ")[0] if not pd.isna(row["artist_string"]) else ""

                    # Use full artist_string as photographer/director
                    # artist = row["artist_string"] if not pd.isna(row["artist_string"]) else ""
                if import_date and (overwrite or not entity.get("date")):
                    metadata["date"] = row["created_at"] if not pd.isna(row["created_at"]) else ""

                if import_details and (overwrite or not entity.get("details")):
                    metadata["details"] = row["description"] if not pd.isna(row["description"]) else ""

                if import_tags and (overwrite or not entity.get("tag_ids")):
                    tag_string = row['tag_string'] if not pd.isna(row['tag_string']) else ""
                    tag_ids, tag_log = process_tags(tag_string)
                    log.extend(tag_log)

                    # Count tag operations
                    created_tags_count += sum(1 for entry in tag_log if "created" in entry.lower())
                    skipped_tags_count += sum(1 for entry in tag_log if "already exists" in entry.lower())
                    
                    metadata["tag_ids"] = tag_ids

                if import_url and (overwrite or not entity.get("url")):
                    metadata["url"] = row["post_url"] if not pd.isna(row["post_url"]) else ""

                # Update metadata for the found entity
                if entity_type == "Image":
                    if import_artist and (overwrite or not entity.get("photographer")):
                        metadata["photographer"] = artist
                    write_to_backup_file(entity, "image", backup_file)
                    update_image_metadata(metadata)
                elif entity_type == "Scene":
                    if import_artist and (overwrite or not entity.get("director")):
                        metadata["director"] = artist
                    write_to_backup_file(entity, "scene", backup_file)
                    update_scene_metadata(metadata)

                updated_count += 1
                log.append(f"{entity_type} {checksum}: Updated successfully.")
            else:
                skipped_files_count += 1
                log.append(f"{entity_type} {checksum}: Not found in Stash DB.")

            # Update progress bar and metrics
            pbar.update(1)
            pbar.set_postfix(OrderedDict([
                ("updated", updated_count),
                ("skipped", skipped_files_count),
                ("tags_created", created_tags_count),
                ("tags_skipped", skipped_tags_count)
            ]))

    # Save log to a file
    with open(log_file, "w") as logf:
        logf.write("\n".join(log))
    print("Processing complete.")
    print(f"Log saved to {log_file}.")
    print(f"Backup saved to {backup_file}.")

def main():
    # Get data directory from config
    gallery_path = CONFIG.get("data_directory")

    # Check if the path is valid
    if not gallery_path or not os.path.isdir(gallery_path):
        print(f"Error: Data directory '{gallery_path}' not found or invalid.")
        sys.exit(1)

    print(f"Data directory validated: {gallery_path}")
    
    # Fetch the latest dump URLs
    dump_urls = get_latest_dump_urls()
    if not dump_urls or not dump_urls.get("posts") or not dump_urls.get("tags"):
        print("Could not fetch the latest database dump URL. Exiting.")
        sys.exit(1)
    
    # Construct the full save paths for the files
    posts_dump_file_name = dump_urls.get("posts").split("/")[-1]
    tags_dump_file_name = dump_urls.get("tags").split("/")[-1]
    posts_dump_save_path = posts_dump_file_name # Save in project directory
    tags_dump_save_path = tags_dump_file_name # Save in project directory
    
    # Download the posts dump file; skip if already downloaded
    if os.path.exists(posts_dump_save_path):
        print(f"Database dump already downloaded: {posts_dump_save_path}")
    else:
        print("Starting the download of the latest database dump...")
        download_file(dump_urls.get("posts"), posts_dump_save_path)

    # Download the tags dump file; skip if already downloaded
    if os.path.exists(tags_dump_save_path):
        print(f"Database dump already downloaded: {tags_dump_save_path}")
    else:
        print("Starting the download of the latest database dump...")
        download_file(dump_urls.get("tags"), tags_dump_save_path)

    output_csv_name = "e621_metadata.csv"
    output_csv_path = output_csv_name # Save in project directory
    #output_csv_path = os.path.join(gallery_path, output_csv_name) # Save in gallery directory

    if os.path.exists(output_csv_path):
        print(f"Output CSV file already exists: {output_csv_path}")
    else:
        print("Processing gallery directory and updating metadata...")
        process_directory(gallery_path, posts_dump_save_path, tags_dump_save_path,
                          output_csv_path, export_json=False, gen_url_col=True, gen_artist_col=True,
                          gen_oshash_col=True)

    print("Processing CSV file and updating metadata in Stash...")
    process_csv_and_update_metadata(output_csv_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
