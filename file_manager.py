import json
import os
import shutil

def read_json(file_path):
    """Read JSON data from a file."""
    try:
        if not os.path.exists(file_path):
            print(f"Error: {file_path} does not exist.")
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON from {file_path}: {e}")
        return None

def save_json(data, file_path):
    """Save JSON data to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Saved JSON to {file_path}")
    except Exception as e:
        print(f"Error saving JSON to {file_path}: {e}")

def update_json_value(file_path, keys, new_value):
    """Change a specific value in the JSON file and update it."""
    try:
        data = read_json(file_path)
        if data is None:
            return

        # Navigate to the correct key and update
        current = data
        for key in keys[:-1]:
            if key in current:
                current = current[key]
            else:
                print(f"Key {key} not found in {file_path}")
                return
        
        final_key = keys[-1]
        if final_key in current:
            current[final_key] = new_value
            save_json(data, file_path)
            print(f"Updated value for {keys} to {new_value} in {file_path}")
        else:
            print(f"Key {final_key} not found in {file_path}")
    except Exception as e:
        print(f"Error updating JSON value in {file_path}: {e}")

def append_json_data(file_path, key, new_data):
    """Append new data to an existing list in the JSON file."""
    try:
        data = read_json(file_path)
        if data is None:
            return

        if key in data and isinstance(data[key], list):
            data[key].append(new_data)
            save_json(data, file_path)
            print(f"Appended new data to {key} in {file_path}")
        elif key in data and isinstance(data[key], dict):
            data[key].update(new_data)
            save_json(data, file_path)
            print(f"Updated dictionary {key} in {file_path}")
        else:
            print(f"Key {key} not found or is not a list/dict in {file_path}")
    except Exception as e:
        print(f"Error appending JSON data to {file_path}: {e}")

def copy_file(src, dest):
    """Copy a file from one folder to another."""
    try:
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"Copied {src} to {dest}")
        else:
            print(f"Error: {src} does not exist.")
    except Exception as e:
        print(f"Error copying {src} to {dest}: {e}")

def rename_file(old_name, new_name):
    """Rename a file safely (overwriting if destination exists)."""
    try:
        if os.path.exists(old_name):
            os.replace(old_name, new_name)
            print(f"Renamed {old_name} to {new_name}")
        else:
            print(f"Error: {old_name} does not exist.")
    except Exception as e:
        print(f"Error renaming {old_name} to {new_name}: {e}")

def delete_file(file_path):
    """Delete a file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
        else:
            print(f"Error: {file_path} does not exist.")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
