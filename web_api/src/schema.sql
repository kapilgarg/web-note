DROP TABLE IF EXISTS note;


CREATE TABLE note (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  note TEXT NOT NULL,
  source TEXT,
  tags TEXT,
  comments TEXT,
  created_on TEXT,
  modified_on TEXT
);