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
('Which of the following is not a cardinal sign of inflammation?', 'Redness', 'Swelling', 'Fever', 'Pain', 'Fever', 'Fever is not a cardinal sign of inflammation.', 1);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is the primary purpose of inflammation?', 'To eliminate the initial cause of cell injury', 'To cause pain', 'To slow down blood flow', 'To cool down the body', 'To eliminate the initial cause of cell injury', 'The primary purpose of inflammation is to eliminate the initial cause of cell injury.', 1);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What are granulocytes?', 'A type of white blood cell', 'A type of red blood cell', 'A type of platelet', 'None of the above', 'A type of white blood cell', 'Granulocytes are a type of white blood cell involved in inflammation.', 1);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is atrophy?', 'Decrease in cell size', 'Increase in cell size', 'Increase in cell number', 'Formation of new cells', 'Decrease in cell size', 'Atrophy is a decrease in cell size.', 2);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is metaplasia?', 'Change from one type of cell to another', 'Increase in cell size', 'Decrease in cell number', 'Cell death', 'Change from one type of cell to another', 'Metaplasia is the change from one type of cell to another.', 2);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is apoptosis?', 'Programmed cell death', 'Uncontrolled cell growth', 'Formation of new cells', 'Decrease in cell size', 'Programmed cell death', 'Apoptosis is the process of programmed cell death.', 2);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is the main function of macrophages?', 'Phagocytosis', 'Cell division', 'Protein synthesis', 'DNA replication', 'Phagocytosis', 'The main function of macrophages is phagocytosis.', 3);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is an example of a chronic inflammatory disease?', 'Rheumatoid arthritis', 'Acute bronchitis', 'Seasonal flu', 'Food poisoning', 'Rheumatoid arthritis', 'Rheumatoid arthritis is an example of a chronic inflammatory disease.', 3);

INSERT INTO Questions (content, option_a, option_b, option_c, option_d, correct_option, explaination, chapter_id) VALUES 
('What is the role of cytokines in inflammation?', 'They act as signaling molecules', 'They provide structural support', 'They transport oxygen', 'They store energy', 'They act as signaling molecules', 'Cytokines act as signaling molecules in the inflammatory response.', 3);


-- Progress
INSERT INTO Progress (user_id, question_id, answer, is_correct) VALUES (1, 1, 'A', 1);
INSERT INTO Progress (user_id, question_id, answer, is_correct) VALUES (2, 2, 'B', 1);

-- currentState
INSERT INTO currentState (user_id, chapter_id, chapter_title, question_id) VALUES (1, 1, 'Chapter 1: Introduction to Pathology', 1);
INSERT INTO currentState (user_id, chapter_id, chapter_title, question_id) VALUES (2, 2, 'Chapter 2: Cellular Adaptations', 2);