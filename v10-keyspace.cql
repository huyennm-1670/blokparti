CREATE TABLE playlists
(
    id               timeuuid,
    creator_id       uuid /* refers to users.id */,
    updated_at       timestamp,
    title            text,
    description      text,
    cover_urls       list<text> /* made from playlist_items.cover_url */,
    selected_item_id uuid,
    PRIMARY KEY (id)
);
--
CREATE TABLE playlist_items
(
    playlist_id        uuid,
    id                 timeuuid,
    order_rank         text,
    data_source_id     uuid,
    source_playlist_id uuid,
    cover_url          text /* made from data source or track image */,
    PRIMARY KEY (playlist_id, id)
) WITH CLUSTERING ORDER BY (id DESC);

CREATE MATERIALIZED VIEW mv_playlist_items_by_order_rank AS
SELECT playlist_id, id, order_rank, data_source_id, source_playlist_id, cover_url
FROM playlist_items
WHERE order_rank IS NOT NULL
  AND id IS NOT NULL
PRIMARY KEY (playlist_id, order_rank, id)
WITH CLUSTERING ORDER BY (order_rank ASC);

CREATE MATERIALIZED VIEW view_playlist_item_by_id AS
    SELECT *
    FROM playlist_items
    WHERE id IS NOT null
    PRIMARY KEY (id, playlist_id)
    WITH CLUSTERING ORDER BY (playlist_id ASC);
--
CREATE TABLE auto_playlists
(
    playlist_id              uuid,
    start_at                 timestamp,
    scheduled_until          timestamp,
    updated_at               timestamp,
    PRIMARY KEY (playlist_id)
);
--
CREATE TABLE party_played_items (
    party_id uuid,
    played_at timestamp,
    cover_url text,
    data_source_id uuid,
    id uuid,
    order_rank text,
    playlist_id uuid,
    source_playlist_id uuid,
    updated_at timestamp,
    PRIMARY KEY (party_id, played_at)
) WITH CLUSTERING ORDER BY (played_at ASC);
--
CREATE TABLE accounts
(
    id            timeuuid,
    email         text,
    date_of_birth date,
    inviter_id    uuid,
    phone         text,
    password      text,
    registration_tokens set<text>,
    salt          text,
    updated_at    timestamp,
    valid         tinyint,
    PRIMARY KEY (id)
);

CREATE INDEX idx_account_by_phone ON accounts (phone);
CREATE INDEX idx_account_by_email ON accounts (email);

INSERT INTO accounts (id, email, valid, updated_at)
VALUES (9107cd00-c311-11eb-8080-808080808080, 'system.backend@blokparti.es', 1, '2021-06-30T08:00:00+00:00');
--
CREATE TABLE users
(
    id         timeuuid,
    account_id uuid,
    bio text,
    cover_image_uri text,
    icon_uri text,
    resized_icon_uri text,
    label int,
    updated_at timestamp,
    username   text,
    valid      tinyint,
    vocation_id tinyint,
    PRIMARY KEY (id)
);

CREATE MATERIALIZED VIEW view_users_in_account AS 
    SELECT * 
    FROM users 
    WHERE account_id IS NOT null 
    PRIMARY KEY (account_id, id) 
    WITH CLUSTERING ORDER BY (id ASC);

INSERT INTO users (account_id, id, username, valid, updated_at)
VALUES (9107cd00-c311-11eb-8080-808080808080, c3b2ec0f-c313-11eb-7f7f-7f7f7f7f7f7f, 'system.backend', 1,
        '2021-06-30T08:00:01+00:00');
--
CREATE TABLE user_sessions
(
    id         timeuuid,
    user_id    uuid,
    account_id uuid,
    device_uid text,
    expires_at timestamp,
    PRIMARY KEY (id)
);
CREATE INDEX idx_sessions_account_id ON user_sessions (account_id) ;
--
CREATE TABLE messages (
    conversation_id uuid,
    id bigint,
    user_id uuid,
    content text,
    conversation_type text,
    edited boolean,
    files list<text>,
    message_type text,
    updated_at timestamp,
    created_at timestamp,
    PRIMARY KEY (conversation_id, id)
) WITH CLUSTERING ORDER BY (id DESC);
--
CREATE TABLE blocks (
    id timeuuid PRIMARY KEY,
    cover_image_uri text,
    creator_id uuid,
    description text,
    icon_uri text,
    name text,
    resized_icon_uri text,
    short_id text,
    updated_at timestamp
);
--
CREATE TABLE block_user (
    block_id uuid,
    user_id uuid,
    created_at timestamp,
    role text,
    status text,
    updated_at timestamp,
    PRIMARY KEY (block_id, user_id)
);
CREATE MATERIALIZED VIEW view_blocks_by_user AS
    SELECT *
    FROM block_user
    WHERE user_id IS NOT null AND status IS NOT null
    PRIMARY KEY (user_id, status, block_id)
    WITH CLUSTERING ORDER BY (status ASC, block_id ASC);
--
CREATE TABLE parties (
    id timeuuid PRIMARY KEY,
    audience_size int,
    begin_time timestamp,
    block_id uuid,
    cover_image_uri text,
    creator_id uuid,
    description text,
    dj_setlist uuid,
    end_time timestamp,
    icon_uri text,
    resized_icon_uri text,
    mode text,
    name text,
    playlist_id uuid,
    start_time timestamp,
    status text,
    updated_at timestamp
);
CREATE MATERIALIZED VIEW view_parties_in_block AS
    SELECT *
    FROM parties
    WHERE block_id IS NOT null
    PRIMARY KEY (block_id, id)
    WITH CLUSTERING ORDER BY (id ASC);
CREATE MATERIALIZED VIEW view_parties_by_mode AS
    SELECT *
    FROM parties
    WHERE mode IS NOT null
    PRIMARY KEY (mode, id)
    WITH CLUSTERING ORDER BY (id ASC);
--
CREATE TABLE party_user (
    party_id uuid,
    user_id uuid,
    attendance_status text,
    created_at timestamp,
    ext map<text, text>,
    invitation_code text,
    invitee_ids set<uuid>,
    role text,
    updated_at timestamp,
    PRIMARY KEY (party_id, user_id)
);
CREATE MATERIALIZED VIEW view_parties_by_user AS
    SELECT *
    FROM party_user
    WHERE user_id IS NOT null AND role IS NOT null
    PRIMARY KEY (user_id, role, party_id)
    WITH CLUSTERING ORDER BY (role ASC, party_id ASC);
CREATE MATERIALIZED VIEW view_party_invitation_code AS
    SELECT *
    FROM party_user
    WHERE invitation_code IS NOT null AND user_id IS NOT null
    PRIMARY KEY (invitation_code, party_id, user_id)
    WITH CLUSTERING ORDER BY (party_id ASC, user_id ASC);
CREATE MATERIALIZED VIEW view_user_role_by_party AS
    SELECT *
    FROM party_user
    WHERE user_id IS NOT null AND role IS NOT null
    PRIMARY KEY (user_id, role, party_id);
--
CREATE TABLE countries (
    code text,
    dial_code text,
    flag_uri text,
    name text,
    updated_at timestamp,
    PRIMARY KEY (code)
);
--
CREATE TABLE friends (
    user_id uuid,
    friend_id uuid,
    status text,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY (user_id, friend_id)
) WITH CLUSTERING ORDER BY (friend_id ASC);
CREATE TABLE task_time_marks
(
    unique_key text,
    task_type text,
    time_mark timestamp,
    PRIMARY KEY (unique_key, task_type)
);
--
CREATE TABLE api_versions (
    version text,
    date timestamp,
    revision tinyint,
    PRIMARY KEY (version, date)
) WITH CLUSTERING ORDER BY (date DESC);
INSERT INTO api_versions (version, date, revision) VALUES ('1.0.1', '2021-10-26 16:58:04+0000', 01);
--
CREATE TABLE party_boot (
    booter_id uuid,
    booted_id uuid,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY (booter_id, booted_id)
) WITH CLUSTERING ORDER BY (booted_id ASC);
--
CREATE TABLE block_building_level (
    building_level text,
    members_count int,
    created_at timestamp,
    icon_uri text,
    resized_icon_uri text,
    updated_at timestamp,
    PRIMARY KEY (building_level, members_count)
) WITH CLUSTERING ORDER BY (members_count ASC);
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_1', 3, '2021-11-17 05:12:44', 'block/building_level_1_1.jpg', '{"default": {"url": "block/building_level_1_1.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_1.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_1.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_1.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_2', 6, '2021-11-17 05:12:44', 'block/building_level_1_2.jpg', '{"default": {"url": "block/building_level_1_2.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_2.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_2.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_2.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_3', 10, '2021-11-17 05:12:44', 'block/building_level_1_3.jpg', '{"default": {"url": "block/building_level_1_3.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_3.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_3.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_3.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_4', 15, '2021-11-17 05:12:44', 'block/building_level_1_4.jpg', '{"default": {"url": "block/building_level_1_4.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_4.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_4.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_4.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_5', 20, '2021-11-17 05:12:44', 'block/building_level_1_5.jpg', '{"default": {"url": "block/building_level_1_5.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_5.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_5.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_5.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_6', 30, '2021-11-17 05:12:44', 'block/building_level_1_6.jpg', '{"default": {"url": "block/building_level_1_6.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_6.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_6.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_6.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_7', 40, '2021-11-17 05:12:44', 'block/building_level_1_7.jpg', '{"default": {"url": "block/building_level_1_7.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_7.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_7.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_7.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_8', 50, '2021-11-17 05:12:44', 'block/building_level_1_8.jpg', '{"default": {"url": "block/building_level_1_8.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_8.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_8.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_8.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_9', 60, '2021-11-17 05:12:44', 'block/building_level_1_9.jpg', '{"default": {"url": "block/building_level_1_9.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_9.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_9.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_9.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
INSERT INTO block_building_level (building_level, members_count, created_at, icon_uri, resized_icon_uri, updated_at) VALUES ('1_10', 70, '2021-11-17 05:12:44', 'block/building_level_1_10.jpg', '{"default": {"url": "block/building_level_1_10.jpg", "width": 512, "height": 512, "mime_type": "jpeg"}, "tiny": {"url": "block/building_level_1_10.tiny.jpg", "width": 80, "height": 80, "mime_type": "jpeg"}, "small": {"url": "block/building_level_1_10.small.jpg", "width": 160, "height": 160, "mime_type": "jpeg"}, "medium": {"url": "block/building_level_1_10.medium.jpg", "width": 320, "height": 320, "mime_type": "jpeg"}}', '2021-11-17 05:12:44');
--
CREATE TABLE last_activity (
    user_id timeuuid,
    updated_at timestamp,
    PRIMARY KEY (user_id)
);
--