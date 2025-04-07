use motionmax;

DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Subscription;
DROP TABLE IF EXISTS Workout_Exercise_Template;
DROP TABLE IF EXISTS Exercise_Template_Meta_Data;
DROP TABLE IF EXISTS Exercise_Meta_Data;
DROP TABLE IF EXISTS Exercise_Template;
DROP TABLE IF EXISTS Workout_Template;
DROP TABLE IF EXISTS RecipeIngredient;
DROP TABLE IF EXISTS Recipe;
DROP TABLE IF EXISTS message_board;
DROP TABLE IF EXISTS Trainer_Meta_Data;
DROP TABLE IF EXISTS Ingredients;

CREATE TABLE Trainer_Meta_Data (
    train_id INT NOT NULL,
    bio TEXT NOT NULL,
    elev_pitch TEXT,
    bank_account_number INT NOT NULL,
    bank_routing_number INT NOT NULL,
    subscription_price FLOAT NOT NULL,
    PRIMARY KEY(train_id),
    FOREIGN KEY (train_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Workout_Template (
    w_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    title CHAR(255) NOT NULL,
    description VARCHAR(2000),
    PRIMARY KEY(w_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Exercise_Template (
    et_id INT NOT NULL AUTO_INCREMENT,
    rep_low INT NOT NULL,
    rep_high INT NOT NULL,
    sets INT NOT NULL,
    PRIMARY KEY(et_id)
);

CREATE TABLE Exercise_Meta_Data (
    emd_id INT NOT NULL AUTO_INCREMENT,
    title CHAR(255) NOT NULL,
    description VARCHAR(2000),
    PRIMARY KEY(emd_id)
);

CREATE TABLE Workout_Exercise_Template (
    w_id INT NOT NULL,
    et_id INT NOT NULL,
    sequence INT,
    PRIMARY KEY (w_id, et_id),
    FOREIGN KEY (w_id) REFERENCES Workout_Template(w_id) ON DELETE CASCADE,
    FOREIGN KEY (et_id) REFERENCES Exercise_Template(et_id) ON DELETE CASCADE
);

CREATE TABLE Exercise_Template_Meta_Data (
    et_id INT NOT NULL,
    emd_id INT NOT NULL,
    PRIMARY KEY (et_id, emd_id),
    FOREIGN KEY (et_id) REFERENCES Exercise_Template(et_id) ON DELETE CASCADE,
    FOREIGN KEY (emd_id) REFERENCES Exercise_Meta_Data(emd_id) ON DELETE CASCADE
);

CREATE TABLE Recipe (
    r_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    title CHAR(255) NOT NULL,
    description VARCHAR(2000),
    calories INT NOT NULL,
    protein INT NOT NULL,
    carbs INT NOT NULL,
    fat INT NOT NULL,
    PRIMARY KEY(r_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Ingredients (
    ing_id INT NOT NULL AUTO_INCREMENT,
    title CHAR(255),
    PRIMARY KEY(ing_id)
);

CREATE TABLE RecipeIngredient (
    r_id INT NOT NULL,
    ing_id INT NOT NULL,
    amount FLOAT,
    measurement VARCHAR(10),
    PRIMARY KEY(r_id, ing_id),
    FOREIGN KEY (r_id) REFERENCES Recipe(r_id) ON DELETE CASCADE,
    FOREIGN KEY (ing_id) REFERENCES Ingredients(ing_id) ON DELETE CASCADE
);

CREATE TABLE Subscription (
    creator_id INT NOT NULL,
    subscriber_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (creator_id, subscriber_id, created_at),
    FOREIGN KEY (creator_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (subscriber_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Message (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    receiver_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (receiver_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES User(user_id) ON DELETE CASCADE
);
