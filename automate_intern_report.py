import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from timedelta_formatter import strfdelta
import numpy as np
import pandas as pd
from create_connection import get_data
from userlist import blokparti_user_list

get_data()
gsheet_url = "https://docs.google.com/spreadsheets/d/1qxoNvkSvDfmIhoJgs9XFucN01kCZsd-1TkVJSzRj-CA/edit#gid=839949834"

# import data
accounts = pd.read_csv("csv_files/accounts.csv", encoding="utf-8", dtype={"phone": str})
parties = pd.read_csv(
    "csv_files/parties.csv",
    encoding="utf-8",
    parse_dates=["begin_time", "end_time", "start_time", "updated_at"],
)
party_user = pd.read_csv(
    "csv_files/party_user.csv",
    encoding="utf-8",
    parse_dates=["created_at", "updated_at"],
)
users = pd.read_csv("csv_files/users.csv", encoding="utf-8")
user_sessions = pd.read_csv("csv_files/user_sessions.csv", encoding="utf-8")
party_played_items = pd.read_csv(
    "csv_files/party_played_items.csv",
    encoding="utf-8",
    parse_dates=["played_at", "updated_at"],
)
messages = pd.read_csv(
    "csv_files/messages.csv", encoding="utf-8", parse_dates=["created_at"]
)

# count number of parties host and duration
dff = pd.merge(
    party_user[["party_id", "user_id", "created_at", "role", "updated_at"]],
    parties[["id", "begin_time", "end_time", "updated_at", "creator_id"]],
    how="left",
    left_on="party_id",
    right_on="id",
)
del dff["id"]

dff.columns = [
    "party_id",
    "user_id",
    "user_party_created_at",
    "role",
    "user_party_updated_at",
    "party_begin_time",
    "party_end_time",
    "party_updated_at",
    "creator_id",
]
dff_ = pd.merge(
    dff,
    users[["id", "account_id", "username"]],
    how="left",
    left_on="user_id",
    right_on="id",
)
del dff_["id"]
dff_ = pd.merge(
    dff_,
    users[["id", "account_id", "username"]],
    how="left",
    left_on="creator_id",
    right_on="id",
    suffixes=("_pu", "_creator"),
)
del dff_["id"]


def party_duration(row):
    if row["role"] == "guest":
        if row["user_party_updated_at"] is pd.NaT and row["party_end_time"] is pd.NaT:
            return row["party_updated_at"] - row["user_party_created_at"]
        elif (
            row["user_party_updated_at"] is pd.NaT
            and row["party_end_time"] is not pd.NaT
        ):
            return row["party_end_time"] - row["user_party_created_at"]
        elif (
            row["user_party_updated_at"] is not pd.NaT
            and row["party_end_time"] is not pd.NaT
        ):
            return row["user_party_updated_at"] - row["user_party_created_at"]
        else:
            return pd.NaT
    elif row["role"] == "host":
        if row["party_end_time"] is pd.NaT:
            return row["party_updated_at"] - row["party_begin_time"]
        else:
            return row["party_end_time"] - row["party_begin_time"]


dff_["party_duration"] = dff_.apply(party_duration, axis=1)
dff_ = dff_.dropna(subset=["party_duration"])
dff_["start_date"] = dff_["party_begin_time"].dt.date
dff_ = pd.merge(
    dff_,
    accounts[["id", "phone"]],
    how="left",
    left_on="account_id_pu",
    right_on="id",
)
del dff_["id"]

df = dff_[~(dff_["phone"].isin(blokparti_user_list)) & (dff_["party_begin_time"] > "2021-11-29")].copy()
df["week"] = df["party_begin_time"].dt.isocalendar().week
df["year"] = df["party_begin_time"].dt.isocalendar().year

# starts pivoting
basic_dff = pd.pivot_table(
    df,
    index=["start_date", "week", "year", "username_pu", "phone"],
    values=["party_id", "party_duration"],
    aggfunc={"party_duration": np.sum, "party_id": len},
    columns="role",
)
basic_dff = basic_dff.reset_index()
basic_dff.columns = ["_".join(a) for a in basic_dff.columns.to_flat_index()]
basic_dff.party_duration_guest = basic_dff.party_duration_guest.fillna(
    np.timedelta64(0)
)
basic_dff.party_duration_host = basic_dff.party_duration_host.fillna(np.timedelta64(0))
basic_dff["all_duration"] = (
    basic_dff.party_duration_guest + basic_dff.party_duration_host
)


def time_range(timed):
    if timed < np.timedelta64(30, "m"):
        return "< 30m"
    elif timed < np.timedelta64(60, "m"):
        return "30m-60m"
    else:
        return ">1h"


basic_dff["duration_range"] = basic_dff["all_duration"].apply(time_range)

fmt = "{D} days {H}h{M}m{S}s"
basic_dff["party_duration_guest_text"] = basic_dff.party_duration_guest.apply(
    lambda x: strfdelta(x, fmt)
)
basic_dff["party_duration_host_text"] = basic_dff.party_duration_host.apply(
    lambda x: strfdelta(x, fmt)
)
basic_dff["all_duration_text"] = basic_dff.all_duration.apply(lambda x: strfdelta(x, fmt))

#turn timedelta into seconds
basic_dff["party_duration_guest"] = basic_dff.party_duration_guest.dt.total_seconds()
basic_dff["party_duration_host"] = basic_dff.party_duration_host.dt.total_seconds()
basic_dff["all_duration"] = basic_dff.all_duration.dt.total_seconds()

basic_dff = basic_dff.sort_values(["start_date_", "username_pu_"], ascending=False)
basic_dff = basic_dff.replace("0 days 0h0m0s", "")
gc = gspread.service_account()
sh = gc.open_by_url(gsheet_url)
worksheet = sh.worksheet("Detail")

intern_names = get_as_dataframe(
    sh.worksheet("Intern_name"),
    dtype={"phone_": str},
    usecols=[0, 1, 2, 3],
    skip_blank_line=True,
    evaluate_formulas=True,
)
basic_dff_ = pd.merge(
    basic_dff,
    intern_names,
    how="left",
    left_on=["username_pu_", "phone_"],
    right_on=["username", "phone_"],
)
basic_dff_ = basic_dff_[
    [
        "week_",
        "year_",
        "start_date_",
        "username_pu_",
        "phone_",
        "name",
        "party_id_host",
        "party_id_guest",
        "party_duration_host_text",
        "party_duration_guest_text",
        "all_duration_text",
        "party_duration_host",
        "party_duration_guest",
        "all_duration",
        "duration_range",
    ]
]
set_with_dataframe(worksheet, basic_dff_, row=2, col=2, include_column_header=False)

#get party hosts
dfd = df.sort_values(["start_date", "username_pu", "username_creator"], ascending=False)[["start_date","username_pu", "role", "username_creator"]]
dfd = dfd[dfd.role=="guest"].drop_duplicates()
dfd['party_host'] = dfd.groupby(['start_date', "username_pu"])['username_creator'].transform(lambda x : ', '.join(x))
dfdf = pd.merge(basic_dff_, dfd, how="left", left_on=["username_pu_", "start_date_"], right_on=["username_pu", "start_date"])
dfdf = dfdf[["start_date_", "username_pu_", "party_host"]].drop_duplicates()
set_with_dataframe(
    worksheet, dfdf[["party_host"]], row=2, col=20, include_column_header=False
)

# participants
participants = pd.pivot_table(
    df,
    index=["start_date", "username_creator"],
    values=["user_id"],
    aggfunc=len,
    columns="role",
).reset_index()

participants.columns = ["_".join(a) for a in participants.columns.to_flat_index()]
participants = participants.sort_values(
    ["start_date_", "username_creator_"], ascending=False
)
dfg = pd.merge(
    basic_dff,
    participants,
    how="left",
    left_on=["username_pu_", "start_date_"],
    right_on=["username_creator_", "start_date_"],
)
set_with_dataframe(
    worksheet, dfg[["user_id_guest"]], row=2, col=17, include_column_header=False
)

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
message_ = message_[~message_.phone.isin(blokparti_user_list)]

message_df = pd.pivot_table(
    message_, index=["message_date", "username"], values="message_id", aggfunc=len
)
message_df = message_df.reset_index().sort_values(
    ["message_date", "username"], ascending=False
)
message_df = pd.merge(
    basic_dff,
    message_df[["message_date", "username", "message_id"]],
    how="left",
    left_on=["start_date_", "username_pu_"],
    right_on=["message_date", "username"],
)
set_with_dataframe(
    worksheet, message_df[["message_id"]], row=2, col=18, include_column_header=False
)

# playlist_items
playlist_df = pd.merge(
    df,
    party_played_items[["party_id", "played_at", "id", "updated_at"]],
    how="left",
    left_on="party_id",
    right_on="party_id",
)

playlist_pivot = (
    pd.pivot_table(
        playlist_df, index=["start_date", "username_pu"], values="id", aggfunc=len
    )
    .reset_index()
    .sort_values(["start_date", "username_pu"], ascending=False)
)
playlist_gf = pd.merge(
    basic_dff,
    playlist_pivot,
    how="left",
    left_on=["start_date_", "username_pu_"],
    right_on=["start_date", "username_pu"],
)
set_with_dataframe(
    worksheet, playlist_gf[["id"]], row=2, col=19, include_column_header=False
)




