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