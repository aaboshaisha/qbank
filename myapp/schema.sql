DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS Chapters;
DROP TABLE IF EXISTS Progress;



CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_paid BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE Chapters(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE Questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct_option CHAR(1) NOT NULL,
    explaination TEXT,
    chapter_id INTEGER,
    FOREIGN KEY (chapter_id) REFERENCES Chapters(id)
);

CREATE TABLE Progress(
    user_id INTEGER,
    question_id INTEGER,
    answer CHAR(1),
    is_correct BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (question_id) REFERENCES Questions(id),
    PRIMARY KEY (user_id, question_id)
);