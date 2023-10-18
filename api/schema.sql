CREATE TABLE user (
   id TEXT NOT NULL PRIMARY KEY,   
   password_hash TEXT
);

CREATE TABLE message (
   id INTEGER PRIMARY KEY,
   username TEXT,
   mytext TEXT,
   imgUrl TEXT,
   mytime TEXT
);