use motionmax;

DROP TABLE IF EXISTS Demograhics;
DROP TABLE IF EXISTS User_Demographic_Data;
DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS User_Feedback;
DROP TABLE IF EXISTS Sales_Report;
DROP TABLE IF EXISTS Subscription_Sales_Report;
DROP TABLE IF EXISTS User_Engagement;
DROP TABLE IF EXISTS Marketing_Channels;
DROP TABLE IF EXISTS User_Marketing;
DROP TABLE IF EXISTS Users_Engagement_Marketing;

CREATE TABLE Demographics (
    demographics_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL ,
    age INT,
    gender VARCHAR(50),
    cultural_background VARCHAR(255),
    fitness_experience TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE User_Demographic_Data (
    user_id INT NOT NULL ,
    demographics_id INT NOT NULL ,
    PRIMARY KEY (user_id, demographics_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (demographics_id) REFERENCES Demographics(demographics_id) ON DELETE CASCADE
);

CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    app_discovery TEXT NOT NULL,
    app_enjoyment TEXT NOT NULL,
    improvement_suggestions TEXT NOT NULL,
    similar_apps TEXT NOT NULL,
    most_useful_feature TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE User_Feedback (
    user_id INT NOT NULL ,
    feedback_id INT NOT NULL ,
    PRIMARY KEY (user_id, feedback_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (feedback_id) REFERENCES Feedback(feedback_id) ON DELETE CASCADE
);

CREATE TABLE Sales_Report (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date_generated DATE NOT NULL,
    new_subscribers INT NOT NULL,
    cancellations INT NOT NULL,
    revenue_generated DECIMAL(15,2),
    roi DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE User_Engagement (
    engagement_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    click_through_rate DECIMAL(5,2),
    open_rates DECIMAL(5,2),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Marketing_Channels (
    channel_id INT AUTO_INCREMENT PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL UNIQUE,
    user_id INT NOT NULL ,
    budget DECIMAL(15,2),
    conversions INT NOT NULL,
    date datetime DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Promo_Codes (
    promo_code_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL ,
    discount DECIMAL(5,2),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE User_Marketing (
    user_id INT NOT NULL ,
    channel_id INT NOT NULL ,
    PRIMARY KEY (user_id, channel_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES Marketing_Channels(channel_id) ON DELETE CASCADE
);

CREATE TABLE Users_Engagement_Marketing (
    engagement_id INT NOT NULL,
    channel_id INT NOT NULL,
    PRIMARY KEY (engagement_id, channel_id),
    FOREIGN KEY (engagement_id) REFERENCES User_Engagement(engagement_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES Marketing_Channels(channel_id) ON DELETE CASCADE
);
