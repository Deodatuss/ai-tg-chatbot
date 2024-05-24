from pathlib import Path
from pandas import Timestamp


DATA_PATH = Path("data/tts/")
TABLE = {
    "uid": [0],
    "uname": ["root"],
    # "added": [Timestamp("20240524")],
    "added": Timestamp.today(),
    "tokens": [0],
    "generations": [0],
}
USERS_TABLE_FILE = "temp.csv"
