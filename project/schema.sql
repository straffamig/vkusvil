DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    content JSON
);