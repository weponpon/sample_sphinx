import os
from pathlib import Path

def get_root_dir():
    """rootディレクトリの位置を絶対パスとして取得する.
    
    Returns:
        Path: root directory
    """
    return Path(os.path.abspath('../'))
