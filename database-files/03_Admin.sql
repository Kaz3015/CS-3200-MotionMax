-- motionMAX Relational Database - Admin System

USE motionmax;

DROP TABLE IF EXISTS System_Metrics;
DROP TABLE IF EXISTS Activity_Log;
DROP TABLE IF EXISTS Flagged_Content;
DROP TABLE IF EXISTS Exercise_Media;
DROP TABLE IF EXISTS Support_Tickets;

CREATE TABLE Exercise_Media (
    exercise_media_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('video', 'image', 'text') NOT NULL,
    exercise_id INT NOT NULL,

    CONSTRAINT fk_exercise_media_exercise
        FOREIGN KEY (exercise_id) REFERENCES Exercise(exercise_id) ON DELETE CASCADE
);

CREATE TABLE Flagged_Content (
    flag_id INT AUTO_INCREMENT PRIMARY KEY,
    reason TEXT NOT NULL,
    date_flagged DATE NOT NULL,
    status ENUM('pending', 'resolved', 'dismissed') NOT NULL,
    exercise_media INT NOT NULL,
    flagged_by_user INT NOT NULL,
    reviewed_by_admin INT,

    CONSTRAINT fk_flagged_content_exercise_media
        FOREIGN KEY (exercise_media) REFERENCES Exercise_Media(exercise_media_id) ON DELETE CASCADE,

    CONSTRAINT fk_flagged_content_user_flagger
        FOREIGN KEY (flagged_by_user) REFERENCES User(user_id),

    CONSTRAINT fk_flagged_content_user_reviewer
        FOREIGN KEY (reviewed_by_admin) REFERENCES User(user_id)
);

CREATE TABLE Activity_Log (
    activity_log_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    admin INT NOT NULL,

    CONSTRAINT fk_activity_log_admin
        FOREIGN KEY (admin) REFERENCES User(user_id)
);

CREATE TABLE System_Metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    cpu_usage DECIMAL(5,2),
    memory_usage DECIMAL(5,2),
    db_latency DECIMAL(5,2),
    active_users INT,
    activity_log_id INT NOT NULL,

    CONSTRAINT fk_system_metrics_activity_log
        FOREIGN KEY (activity_log_id) REFERENCES Activity_Log(activity_log_id) ON DELETE CASCADE
);

CREATE TABLE Support_Tickets (
    support_ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('open', 'closed', 'in_progress') NOT NULL,
    date_created DATETIME NOT NULL,
    date_resolved DATETIME,
    description TEXT,
    created_by_user INT NOT NULL,
    resolved_by_admin INT,

    CONSTRAINT fk_support_tickets_user_creator
        FOREIGN KEY (created_by_user) REFERENCES User(user_id),

    CONSTRAINT fk_support_tickets_user_resolver
        FOREIGN KEY (resolved_by_admin) REFERENCES User(user_id)
);