import os
import os.path
import urllib.request


def copy_file_from_url(url, fname, mode="wt"):
    """Copies text or binary files from remote website.
    
    Files are copied to Python's current working directory.
    
    Args:
        url: URL of file on remote website.
        fname: name used for saving file on local filesystem
        mode: Use "wt" for text files and "wb" for binary files.
    """
    with urllib.request.urlopen(url) as response:
        text = response.read()
        if mode == "wt":
            text = text.decode("utf-8")
    with open(fname, mode) as local_file:
        local_file.write(text)