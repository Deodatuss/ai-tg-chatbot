import pandas as pd


import constants

USERS_TABLE = constants.DATA_PATH / constants.USERS_TABLE_FILE

if not USERS_TABLE.is_file():
    initial_file = pd.DataFrame(constants.TABLE)
    initial_file.to_csv(constants.DATA_PATH / constants.USERS_TABLE_FILE)

_df_users = pd.read_csv(USERS_TABLE)


###


def get_tokens_by_id(uid: int) -> int:
    global _df_users
    return _df_users.loc[_df_users["uid"] == uid, "tokens"].values[0]


def set_tokens_by_id(uid: int, new_tokens: int) -> None:
    global _df_users
    _df_users.loc[_df_users["uid"] == uid, "tokens"] = new_tokens
    # saving new tokens to secure data
    _df_users.to_csv(constants.DATA_PATH / constants.USERS_TABLE_FILE)


###


def get_gens_by_id(uid: int) -> int:
    global _df_users
    return _df_users.loc[_df_users["uid"] == uid, "generations"].values[0]


def set_gens_by_id(uid: int, new_generations: int) -> None:
    global _df_users
    _df_users.loc[_df_users["uid"] == uid, "generations"] = new_generations
    # saving new generations to secure data
    _df_users.to_csv(constants.DATA_PATH / constants.USERS_TABLE_FILE)


###


def add_user_entry(user_info: dict) -> None:
    global _df_users
    temp_df = pd.DataFrame(user_info)

    _df_users = pd.concat([_df_users, temp_df], ignore_index=True)

    # saving new users to secure data
    _df_users.to_csv(constants.DATA_PATH / constants.USERS_TABLE_FILE)


def is_existing_user(uid: int):
    return uid in _df_users["uid"].values
