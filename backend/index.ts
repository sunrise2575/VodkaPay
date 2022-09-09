import { express } from 'express';
import { path } from 'path';
import * as db from 'better-sqlite3';

const app = express();
const PORT = 8002;

app.get("/init", (req, res) => {
  query = `
  CREATE TABLE IF NOT EXISTS user (
    id BIGINT NOT NULL,
    name BIGINT NOT NULL,
    email BIGINT NOT NULL,
    pw_sha256 TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email)
  )

  CREATE TABLE IF NOT EXISTS event (
    -- writing...
  )

  CREATE TABLE IF NOT EXISTS pay (
    -- writing...
  )

  CREATE TABLE IF NOT EXISTS record (
    timestamp TEXT NOT NULL,
    deptor_id BIGINT NOT NULL,
    creditor_id BIGINT NOT NULL,
    money_id BIGINT NOT NULL,
    memo TEXT DEFAULT NULL,
    UNIQUE (timestamp, deptor_id, creditor_id),
    FOREIGN KEY (deptor_id) REFERENCES user(id),
    FOREIGN KEY (creditor_id) REFERENCES user(id)
  )
  `;
});

app.get("/api/", (req, res) => {
  res.send("hello");
});

app.post("/", (req, res) => {
  res.send("hello");
});

app.use("/", express.static(path.join(__dirname, "../frontend/build/")));
app.listen(PORT, () => console.log(`listen ${PORT}`));
