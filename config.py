from pathlib import Path
from os.path import dirname, abspath


BASE_DIR = Path(dirname(abspath(__file__)))
TMPL_DIR = BASE_DIR / "templates"
DIST_DIR = BASE_DIR / "dist"
