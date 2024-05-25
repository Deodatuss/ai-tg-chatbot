import pandas as pd

from pandas import DataFrame

import constants

USERS_TABLE = constants.DATA_PATH / constants.USERS_TABLE_FILE

if not USERS_TABLE.is_file():
    initial_file = pd.DataFrame(constants.TABLE)
    initial_file.to_csv(constants.DATA_PATH / constants.USERS_TABLE_FILE, index=True)

_df_users = pd.read_csv(USERS_TABLE, index_col=0)


def save_users():
    _df_users.to_csv(constants.DATA_PATH / constants.USERS_TABLE_FILE, index=True)


###


def get_tokens_by_id(uid: int) -> int:
    global _df_users
    return _df_users.loc[uid, "tokens"]


def set_tokens_by_id(uid: int, new_tokens: int) -> None:
    global _df_users
    _df_users.loc[uid, "tokens"] = new_tokens
    # saving new tokens to secure data
    save_users()


###


def get_gens_by_id(uid: int) -> int:
    global _df_users
    return _df_users.loc[uid, "generations"]


def set_gens_by_id(uid: int, new_generations: int) -> None:
    global _df_users
    _df_users.loc[uid, "generations"] = new_generations
    # saving new generations to secure data
    save_users()


###


def add_user_entry(temp_df: DataFrame) -> None:
    global _df_users

    _df_users = pd.concat([_df_users, temp_df], ignore_index=False)

    # saving new users to secure data
    save_users()


def is_existing_user(uid: int):
    return uid in _df_users.index
