import numpy as np
import pandas as pd
from IPython.display import display

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

accounts = pd.read_csv("csv_files/accounts.csv", encoding="utf-8", dtype={"phone": str})
parties = pd.read_csv(
    "csv_files/parties.csv",
    encoding="utf-8",
    parse_dates=["begin_time", "end_time", "start_time", "updated_at"],
)
party_user = pd.read_csv(
    "csv_files/party_user.csv", encoding="utf-8", parse_dates=["created_at", "updated_at"]
)
users = pd.read_csv("csv_files/users.csv", encoding="utf-8")
user_sessions = pd.read_csv("csv_files/user_sessions.csv", encoding="utf-8")
party_played_items = pd.read_csv(
    "csv_files/party_played_items.csv", encoding="utf-8", parse_dates=["played_at", "updated_at"]
)
messages = pd.read_csv("csv_files/messages.csv", encoding="utf-8", parse_dates=["created_at"])


# count number of parties host and duration
dff = pd.merge(
    parties[
        [
            "id",
            "audience_size",
            "begin_time",
            "end_time",
            "creator_id",
            "start_time",
            "status",
            "updated_at",
        ]
    ],
    party_user[
        ["party_id", "user_id", "attendance_status", "created_at", "role", "updated_at"]
    ],
    how="right",
    left_on="id",
    right_on="party_id",
)
dff.columns = [
    "party_id",
    "party_size",
    "party_begin_time",
    "party_end_time",
    "creator_id",
    "party_start_time",
    "party_status",
    "party_updated_at",
    "party_id_",
    "user_id",
    "attendance_status",
    "user_created_at",
    "role",
    "user_updated_at",
]
dff_ = pd.merge(
    dff,
    users[["id", "account_id", "username"]],
    how="left",
    left_on="user_id",
    right_on="id",
)
dff_.columns = [
    "party_id",
    "party_size",
    "party_begin_time",
    "party_end_time",
    "creator_id",
    "party_start_time",
    "party_status",
    "party_updated_at",
    "party_id_",
    "user_id",
    "attendance_status",
    "user_created_at",
    "role",
    "user_updated_at",
    "user_id_",
    "account_id",
    "username",
]
del dff_["party_id_"]
del dff_["user_id_"]


def party_duration(row):
    if row["party_end_time"] is None:
        s = row["party_updated_at"] - row["party_begin_time"]
    else:
        s = row["party_end_time"] - row["party_begin_time"]
    return s


dff_["party_duration"] = dff.apply(party_duration, axis=1)
dff_["party_duration"] = dff_["party_duration"].dt.total_seconds()
dff_["start_date"] = dff_["party_begin_time"].dt.date
dff_ = dff_.sort_values(
    ["username", "start_date", "party_updated_at", "role", "user_updated_at"]
)
dff_ = pd.merge(
    dff_,
    accounts[["id", "email", "phone"]],
    how="left",
    left_on="account_id",
    right_on="id",
)
del dff_["id"]
# dff_.to_csv("dff_.csv", encoding="utf-8")

# message
message = pd.merge(
    parties[["id", "start_time"]],
    messages[["conversation_id", "id", "content", "user_id", "created_at"]],
    how="right",
    left_on="id",
    right_on="conversation_id",
)
message.columns = [
    "party_id",
    "party_start_time",
    "conversation_id",
    "message_id",
    "content",
    "user_id",
    "message_created_at",
]
message = pd.merge(
    message,
    users[["id", "account_id", "username"]],
    how="left",
    left_on="user_id",
    right_on="id",
)
message_ = pd.merge(
    message,
    accounts[["id", "email", "phone"]],
    how="left",
    left_on="account_id",
    right_on="id",
)
del message_["id_x"]
del message_["id_y"]
del message_["email"]
message_["message_date"] = message_["message_created_at"].dt.date
message_.to_csv("message.csv", encoding="utf-8")

# playlist_items
dfff_ = pd.merge(
    dff_,
    party_played_items[["party_id", "played_at", "id", "updated_at"]],
    left_on="party_id",
    right_on="party_id",
)
dfff_.to_csv("with_party_items.csv", encoding="utf-8")
