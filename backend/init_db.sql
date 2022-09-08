CREATE TABLE IF NOT EXISTS users (
    id BIGINT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    pw_sha256 TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS events (
    id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    memo TEXT NOT NULL,
    PRIMARY KEY (id),
);

CREATE TABLE IF NOT EXISTS actions (
    id BIGINT NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id),
);

CREATE TABLE IF NOT EXISTS events_detail (
    event_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    action_id BIGINT NOT NULL,
    money BIGINT NOT NULL,
    UNIQUE (event_id, user_id, action_id),
    FOREIGN KEY (event_id) REFERENCES user(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
    FOREIGN KEY (action_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS overpayments (
    event_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    money BIGINT NOT NULL,
    UNIQUE (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES user(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

INSERT OR IGNORE INTO users (
    name, email, pw_sha_256
) VALUES (
    ?, ?, ?, CURRENT_TIMESTAMP
);

UPDATE users AS u
SET name = ?
WHERE u.id = ? AND u.pw_sha256 = ?;

UPDATE users AS u
SET email = ?
WHERE u.id = ? AND u.pw_sha256 = ?;

UPDATE users AS u
SET pw_sha_256 = ?
WHERE u.id = ? AND u.pw_sha256 = ?;

INSERT OR IGNORE INTO events (memo) VALUES (?);