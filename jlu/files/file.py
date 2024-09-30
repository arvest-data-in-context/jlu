import os
import requests
import zipfile
import mimetypes
from typing import Union, List
from .text_files import *
from .application_files import *
from .video_files import *
from .audio_files import *
from .image_files import *

class File:
    def __init__(self, **kwargs) -> None:
        """
        An object representing any file.
        """

        self.path = kwargs.get("path", None)
        self.filename = kwargs.get("filename", None)
        self.dir = kwargs.get("dir", None)
        self.ext = kwargs.get("ext", None)
        self.mime = kwargs.get("mime", None)

        # If path local given, get filename and directory:
        if self.path != None:
            self.filename = os.path.basename(self.path)
            self.dir = os.path.dirname(self.path)

        # If filename given, get extension and mime type:
        
        if self.filename != None:
            self.ext = os.path.splitext(self.filename)[1][1:]
            self.mime = mimetypes.guess_type(self.filename)[0].split("/")

        self.content = kwargs.get("content", None)

        if kwargs.get("read_content", True):
            if self.filename != None and self.content == None:
                self.read_content(**kwargs.get("read_kwargs", {})) 

    def write(self, **kwargs):
        """Write the contents of the file at its folder under its filename."""

        if self.mime[0] == "image":
            write_image(self)
        elif self.mime[0] == "audio":
            write_audio(self)
        elif self.mime[0] == "video":
            write_video(self)
        elif self.mime[0] == "application":
            if self.mime[1] == "json":
                write_json(self, **kwargs)
            elif self.mime[1] == "xml":
                write_xml(self)
            else:
                self._cannot_write_data()
        elif self.mime[0] == "text":
            if self.mime[1] == "plain":
                write_plain(self)
            elif self.mime[1] == "csv":
                write_csv(self)
            else:
                self._cannot_write_data()
        else:
            self._cannot_write_data()

    def read_content(self, **kwargs):
        """
        Retrive the content of the file, the return type changes according to the type of file.
        """

        if self.mime[0] == "image":
            self.content = read_image(self.path, **kwargs)
        elif self.mime[0] == "audio":
            self.content = read_audio(self.path)
        elif self.mime[0] == "video":
            self.content = read_video(self.path)
        elif self.mime[0] == "application":
            if self.mime[1] == "json":
                self.content = read_json(self.path)
            elif self.mime[1] == "xml":
                self.content = read_xml(self.path)
            else:
                self.content = self._cannot_read_data()
        elif self.mime[0] == "text":
            if self.mime[1] == "plain":
                self.content = read_plain_text(self.path)
            elif self.mime[1] == "csv":
                self.content = read_csv(self.path, **kwargs)
            else:
                self.content = self._cannot_read_data()
        else:
            self.content = self._cannot_read_data()

    def _cannot_read_data(self):
        """Return none when cannot read content."""

        print("This file type is not supported for content retrieval!")
        return None
    
    def _cannot_write_data(self):
        """Feedback for being unable to write content."""

        print("This file type is not supported for content writing!")
        return None

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