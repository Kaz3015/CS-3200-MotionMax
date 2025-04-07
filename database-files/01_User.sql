DROP DATABASE IF EXISTS motionmax;
CREATE DATABASE IF NOT EXISTS motionmax;

use motionmax;

DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Circuit;
DROP TABLE IF EXISTS Exercise;
DROP TABLE IF EXISTS ExerciseSet;
DROP TABLE IF EXISTS WorkoutLog;
DROP TABLE IF EXISTS FoodLog;
DROP TABLE IF EXISTS FoodItem;
DROP TABLE IF EXISTS FoodLog_FoodItem;
DROP TABLE IF EXISTS HealthTips;
DROP TABLE IF EXISTS Motivation;

CREATE TABLE User (
    user_id int AUTO_INCREMENT PRIMARY KEY,
    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    email varchar(255) NOT NULL,
    gender enum('male', 'female', 'other') NOT NULL,
    role enum('client', 'trainer', 'admin', 'salesperson'),
    height_ft int NOT NULL, -- feet part of height
    height_in int NOT NULL, -- inches part of height
    weight decimal(5,2) NOT NULL, -- in pounds
    date_of_birth date NOT NULL,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Attribute Checks
    CONSTRAINT check_height_nonnegative CHECK (height_ft >= 0 AND height_in >=0),
    CONSTRAINT check_user_weight_nonnegative CHECK (weight >= 0)
);

CREATE TABLE Circuit (
    circuit_id int AUTO_INCREMENT PRIMARY KEY,
    user_id int NOT NULL, -- who the circuit is for
    created_by int NOT NULL, -- who creates the circuit
    name varchar(100) NOT NULL,
    description text NOT NULL,
    circuit_type enum('strength', 'cardiovascular', 'flexibility', 'balance') DEFAULT 'strength' NOT NULL,
    difficulty enum('beginner', 'intermediate', 'advanced'),
    target_muscle text NOT NULL,
    equipment_needed text NOT NULL,
    scheduled_date date,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_circuit_user_user_id FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_circuit_user_created_by FOREIGN KEY (created_by) REFERENCES User(user_id) ON DELETE CASCADE

);

CREATE TABLE Exercise (
    exercise_id int AUTO_INCREMENT PRIMARY KEY,
    circuit_id int NOT NULL,
    name varchar(100) NOT NULL,
    description text NOT NULL,
    exercise_type enum('strength', 'cardiovascular', 'flexibility', 'balance') DEFAULT 'strength' NOT NULL,
    difficulty enum('beginner', 'intermediate', 'advanced'),
    target_muscle text NOT NULL,
    equipment_needed text NOT NULL,
    video_url varchar(255) NOT NULL,
    personal_notes text,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_exercise_circuit FOREIGN KEY (circuit_id) REFERENCES Circuit (circuit_id) ON DELETE CASCADE
);

CREATE TABLE ExerciseSet (
    exerciseset_id int AUTO_INCREMENT PRIMARY KEY,
    exercise_id int NOT NULL,
    weight decimal(5, 2),
    reps int, -- if reps are used
    duration_seconds int, -- if time is used
    is_superset boolean DEFAULT FALSE, -- if a superset is being used
    rest_seconds int,
    completed boolean DEFAULT FALSE,
    set_order int,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_exerciseset_exercise FOREIGN KEY (exercise_id) REFERENCES Exercise (exercise_id) ON DELETE CASCADE,

    -- Attribute Checks
    CONSTRAINT check_weight_nonnegative CHECK (weight >= 0),
    CONSTRAINT check_reps_nonnegative CHECK (reps >= 0),
    CONSTRAINT check_duration_seconds_nonnegative CHECK (duration_seconds >= 0),
    CONSTRAINT check_rest_nonnegative CHECK (rest_seconds >= 0),
    CONSTRAINT check_set_order_nonnegative CHECK (set_order >= 0),
    CONSTRAINT check_not_all_recording_options_are_used CHECK (
        ((reps > 0 AND (duration_seconds IS NULL || duration_seconds = 0) AND !is_superset) ||
         ((reps IS NULL || reps = 0) AND duration_seconds > 0 AND !is_superset) ||
         ((reps IS NULL || reps = 0) AND (duration_seconds IS NULL || duration_seconds = 0) AND is_superset))
    )
);

CREATE TABLE WorkoutLog (
    workoutlog_id int AUTO_INCREMENT PRIMARY KEY,
    user_id int NOT NULL,
    circuit_id int,
    datetime_logged datetime NOT NULL,
    duration int,
    description text,
    calories_burned int,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_workoutlog_user FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_workoutlog_circuit FOREIGN KEY (circuit_id) REFERENCES Circuit (circuit_id) ON DELETE CASCADE,

    -- Attribute Checks
    CONSTRAINT check_duration_nonnegative CHECK (duration >= 0),
    CONSTRAINT check_calories_burned_nonnegative CHECK (calories_burned >= 0)
);

CREATE TABLE FoodLog (
    food_log_id int AUTO_INCREMENT PRIMARY KEY,
    user_id int NOT NULL,
    meal_type enum('breakfast', 'lunch', 'dinner', 'snack', 'other') NOT NULL,
    date_logged date NOT NULL,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_foodlog_user FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE
);

CREATE TABLE FoodItem (
    food_item_id int AUTO_INCREMENT PRIMARY KEY,
    name varchar(100) NOT NULL,
    calories int NOT NULL,
    protein decimal(5,2) NOT NULL, -- in grams
    carbs decimal(5,2) NOT NULL, -- in grams
    fats decimal(5,2) NOT NULL, -- in grams
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Attribute Checks
    CONSTRAINT check_calories_nonnegative CHECK (calories >= 0),
    CONSTRAINT check_protein_nonnegative CHECK (protein >= 0),
    CONSTRAINT check_carbs_nonnegative CHECK (carbs >= 0),
    CONSTRAINT check_fats_nonnegative CHECK (fats >= 0)
);

CREATE TABLE FoodLog_FoodItem (
    food_log_item_id int AUTO_INCREMENT PRIMARY KEY,
    food_log_id int NOT NULL,
    food_item_id int NOT NULL,
    servings decimal(5,2) NOT NULL, -- how many was had (quantity)
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign Keys
    CONSTRAINT fk_foodlogitem_foodlog FOREIGN KEY (food_log_id) REFERENCES FoodLog (food_log_id) ON DELETE CASCADE,
    CONSTRAINT fk_foodlogitem_fooditem FOREIGN KEY (food_item_id) REFERENCES FoodItem (food_item_id) ON DELETE CASCADE,

    -- Attribute Checks
    CONSTRAINT check_servings_nonnegative CHECK (servings >= 0)
);

CREATE TABLE HealthTips (
    health_tips_id int AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL,
    text text NOT NULL,
    tip_type enum('nutrition', 'exercise', 'lifestyle', 'mental_health') DEFAULT 'lifestyle',
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Motivation (
    motivation_id int AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL,
    text text NOT NULL,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);