DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS Chapters;
DROP TABLE IF EXISTS Progress;
DROP TABLE IF EXISTS currentState;
-- the commands above will clear any pre-existing tables if we run this script


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


CREATE TABLE currentState(
    user_id INTEGER,
    chapter_id INTEGER,
    chapter_title TEXT,
    question_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (chapter_id) REFERENCES Chapters(id),
    FOREIGN KEY (question_id) REFERENCES Questions(id),
    FOREIGN KEY (chapter_title) REFERENCES Chapters(title),
    PRIMARY KEY (user_id, chapter_id)
);


-- Insert sample data

-- Users
INSERT INTO Users (email, password, is_paid) VALUES ('user1@example.com', 'password1', 1);
INSERT INTO Users (email, password, is_paid) VALUES ('user2@example.com', 'password2', 0);

-- Chapters
INSERT INTO Chapters (title) VALUES ('Chapter 1: Introduction to Pathology');
INSERT INTO Chapters (title) VALUES ('Chapter 2: Cellular Adaptations');
INSERT INTO Chapters (title) VALUES ('Chapter 3: Inflammation and Repair');

-- Questions
INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is pathology?', 'Study of diseases', 'Study of animals', 'Study of plants', 'Study of ecosystems', 'A', 'Pathology is the study of diseases.', 1);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is cellular adaptation?', 'Cell death', 'Change in cell size, number, phenotype', 'Formation of new cells', 'All of the above', 'B', 'Cellular adaptation involves changes in cell size, number, and phenotype.', 2);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is inflammation?', 'A process of healing', 'A process of cell growth', 'A process of cell death', 'A process of blood clotting', 'A', 'Inflammation is a process of healing.', 3);

-- Progress
INSERT INTO Progress (user_id, question_id, answer, is_correct) VALUES (1, 1, 'A', 1);
INSERT INTO Progress (user_id, question_id, answer, is_correct) VALUES (2, 2, 'B', 1);

-- currentState
INSERT INTO currentState (user_id, chapter_id, chapter_title, question_id) VALUES (1, 1, 'Chapter 1: Introduction to Pathology', 1);
INSERT INTO currentState (user_id, chapter_id, chapter_title, question_id) VALUES (2, 2, 'Chapter 2: Cellular Adaptations', 2);