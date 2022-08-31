-- 
CREATE TABLE IF NOT EXISTS user (
    id    BIGINT PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT UNIQUE
)

-- INSERT
INSERT INTO student (
    name, email
) VALUES (
    '이종현', '1428ksu@gmail.com'
)