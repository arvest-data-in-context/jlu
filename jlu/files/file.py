import os
import requests
import zipfile

def download_zip(url, path):
    """Download a zip file and unpack it's contents at the given path (a folder of the filename will be created)."""
    
    # Download file:
    response = requests.get(url)
    temp_zip = os.path.join(path, os.path.basename(url))
    with open(temp_zip, 'wb') as file:
        file.write(response.content)

    # Create the output folder:
    if os.path.isdir(path) == False:
        os.makedirs(path)

    # Unzip:
    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall(path)
    
    # Remove temporary ip file:
    os.remove(temp_zip)

def collect_files(path, acceptedFormats = []):
    """Collect all files of accepted format in a given directory."""

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if len(acceptedFormats) > 0:
                extension = os.path.splitext(file)[1][1:]
                if extension in acceptedFormats:
                    finalList.append(os.path.join(root, file))
            else:
                finalList.append(os.path.join(root, file))
    return finalList

def zip_folder(path, zip_path):
    """Compress a folder as a zip file."""

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))