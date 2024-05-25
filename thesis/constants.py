from pathlib import Path
from pandas import Timestamp, DataFrame


DATA_PATH = Path("data/tts/")
# TABLE = {
#     "uid": [0],
#     "uname": ["root"],
#     # "added": [Timestamp("20240524")],
#     "added": Timestamp.today(),
#     "tokens": [0],
#     "generations": [0],
# }
TABLE = DataFrame(
    [[str("root"), Timestamp.today(), 0, 0]],
    index=[0],
    columns=["uname", "added", "tokens", "generations"],
)
USERS_TABLE_FILE = "users.csv"
