import os
import mimetypes
from .text_files import *
from .application_files import *
from .video_files import *
from .audio_files import *
from .image_files import *
from .utils import get_text_file_properties
import uuid

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
        self.file_properties = None

        # If path local given, get filename and directory:
        if self.path != None:
            self.filename = os.path.basename(self.path)
            self.dir = os.path.dirname(self.path)

        # If filename given, get extension and mime type:
        
        if self.filename != None:
            self.ext = os.path.splitext(self.filename)[1][1:]
            self.mime = mimetypes.guess_type(self.filename)[0].split("/")

        self.content = kwargs.get("content", None)

        if self.path != None and kwargs.get("get_file_properties", False):
            self.get_file_properties()

        if kwargs.get("read_content", True):
            if self.filename != None and self.content == None:
                self.read_content(**kwargs.get("read_kwargs", {})) 

    def get_file_properties(self, **kwargs) -> dict:
        """Update the file's file_properties property and return as dict."""

        if self.mime[0] == "image":
            get_image_properties(self)
        elif self.mime[0] == "audio":
            get_audio_properties(self)
        elif self.mime[0] == "video":
            get_video_properties(self)
        elif self.mime[0] == "application" or self.mime[0] == "text":
            get_text_file_properties(self)
        else:
            self._cannot_get_properties()

        return self.file_properties

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
    
    def _cannot_get_properties(self):
        """Feedback for being unable to get file properties."""

        print("This file type is not supported for retrieving properties!")
        return None
    
def _process_media_get(path, file_list, new_filename, **kwargs):
    """
    Once a file has been retrived, move it and return File objects.
    
    This has been placed here to avoid circular imports (and because is shared in gcu with downloads and uploads).
    """   

    # Create directory if needed
    if os.path.isdir(path) == False:
        os.makedirs(path)

    # Create a list of new names if needed
    new_names = []
    original_folder = os.path.dirname(file_list[0])
    for item in file_list:
        new_names.append(os.path.basename(item))

    # As uuids
    if new_filename == "_uuid":
        new_names = []
        for item in file_list:
            new_names.append(str(uuid.uuid4()) + os.path.splitext(os.path.basename(item))[1])
    
    # As string
    elif isinstance(new_filename, str):
        new_names = []
        if len(file_list) == 1:
            new_names.append(new_filename + os.path.splitext(os.path.basename(file_list[0]))[1])
        else:
            for i, item in enumerate(file_list):
                new_names.append(new_filename + f" {i}" + os.path.splitext(os.path.basename(item))[1])
    
    if path == "":
        path = os.getcwd()
    # Move uploaded files
    for i, item in enumerate(file_list):
        new_path = os.path.join(path, new_names[i])
        os.rename(os.path.join(original_folder, file_list[i]), new_path)

    # Create File objects
    if len(file_list) == 1:
        return File(path = os.path.join(path, new_names[0]), read_content = kwargs.get("read_content", False), read_kwargs = kwargs.get("read_kwargs", {}))
    else:
        ret = []
        for filename in new_names:
            ret.append(File(path = os.path.join(path, filename), read_content = kwargs.get("read_content", False), read_kwargs = kwargs.get("read_kwargs", {})))
        return ret