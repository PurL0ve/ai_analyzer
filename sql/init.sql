CREATE DATABASE ai_analyzer_db;

USE ai_analyzer_db;


CREATE TABLE analysis_history(
    id INT PRIMARY KEY AUTO_INCREMENT,
    position VARCHAR(100),
    user_skills VARCHAR(500),
    required_skills VARCHAR(500),
    rate FLOAT,
    created_time DATETIME
);