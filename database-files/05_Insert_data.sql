use motionmax;

INSERT INTO User(first_name, last_name, email, gender, height_ft, height_in, weight, date_of_birth, role)
VALUES
  ('John', 'Smith', 'john.doe@gmail.com', 'male', 5, 10, 175.50, '1990-01-15', 'trainer'),
  ('Jane', 'Smith', 'jane.smith@gmail.com', 'female', 5, 6, 135.00, '1992-05-20', 'client'),
  ('Alice', 'Brown', 'alice.brown@gmail.com', 'female', 5, 4, 120.25, '1995-08-30', 'client'),
  ('Bob', 'Johnson', 'bob.johnson@gmail.com', 'male', 6, 0, 200.00, '1988-12-10', 'client'),
  ('Charlie', 'Davis', 'charlie.davis@gmail.com', 'other', 5, 9, 160.75, '1998-03-05', 'client');

INSERT INTO Trainer_Meta_Data(train_id, bio, elev_pitch, bank_account_number, bank_routing_number, subscription_price)
VALUES
  (1, 'Experienced personal trainer with a passion for fitness.', 'I help you achieve your goals!', 123456789, 987654321, 29.99);

INSERT INTO Circuit(user_id, created_by, name, description, circuit_type, difficulty, target_muscle, equipment_needed)
VALUES
  (1,1, 'Full Body Blast', 'A full body strength circuit', 'strength', 'beginner', 'all muscles', 'dumbbells, mat'),
  (2,2, 'Cardio Burn', 'High intensity cardio workout', 'cardiovascular', 'intermediate','legs, heart', 'treadmill'),
  (3,3, 'Flex & Stretch', 'Flexibility and balance focused workout', 'flexibility', 'advanced','core muscles', 'yoga mat');

INSERT INTO Exercise (circuit_id, name, description, exercise_type, difficulty, target_muscle, equipment_needed, video_url, personal_notes)
VALUES
  (1, 'Push Ups', 'Standard push ups exercise', 'strength', 'beginner', 'chest, triceps', 'none', 'http://example.com/pushups', 'Keep your back straight.'),
  (2, 'Running', 'Treadmill running exercise', 'cardiovascular', 'intermediate', 'legs, heart', 'treadmill', 'http://example.com/running', 'Warm up before starting.'),
  (3, 'Yoga Stretch', 'Stretching routine for flexibility', 'flexibility', 'advanced', 'core, legs', 'yoga mat', 'http://example.com/yogastretch', 'Focus on breathing.');

INSERT INTO ExerciseSet(exercise_id, weight, reps, duration_seconds, is_superset, rest_seconds, completed, set_order)
VALUES
  (1, 10, 15, 0, FALSE, 30, FALSE, 1),
  (1, 13, 12, 0, FALSE, 30, FALSE, 2),
  (2, 14, 10, 0, FALSE, 60, FALSE, 1),
  (2, 11, 9, 0, FALSE, 60, FALSE, 2),
  (3, 10, 9, 0, FALSE, 30, FALSE, 1);

INSERT INTO WorkoutLog (user_id, circuit_id, datetime_logged, duration, description, calories_burned)
VALUES
  (1, 1, '2025-03-01 08:00:00', 45, 'Morning full body workout', 300),
  (2, 2, '2025-03-02 09:00:00', 30, 'Quick cardio session', 250),
  (3, 3, '2025-03-03 07:30:00', 60, 'Extended flexibility session', 200);

INSERT INTO FoodLog (user_id, meal_type, date_logged)
VALUES
  (1, 'breakfast', '2025-03-01'),
  (2, 'lunch', '2025-03-02'),
  (3, 'dinner', '2025-03-03');

INSERT INTO FoodItem (name, calories, protein, carbs, fats)
VALUES
  ('Oatmeal', 150, 5.50, 27.00, 2.50),
  ('Chicken Breast', 200, 30.00, 0.00, 5.00),
  ('Salad', 100, 3.00, 10.00, 7.00);

INSERT INTO FoodLog_FoodItem (food_log_id, food_item_id, servings)
VALUES
  (1, 1, 1.00),
  (2, 2, 1.50),
  (3, 3, 2.00);

INSERT INTO Workout_Template (user_id, title, description)
VALUES
  (1, 'Morning Routine', 'A simple morning workout'),
  (1, 'Evening Routine', 'An intense evening workout'),
  (1, 'Weekend Blast', 'A mix of strength and cardio');

INSERT INTO Exercise_Template (rep_low, rep_high, sets)
VALUES
  (8, 12, 3),
  (10, 15, 4),
  ( 6, 10, 2);


INSERT INTO Exercise_Meta_Data (title, description)
VALUES
  ('Push Up Variation', 'Modified push-ups with wider hand placement'),
  ('Treadmill Sprint', 'High-speed sprint intervals'),
  ('Yoga Flow', 'Sequence of yoga poses for flexibility');


INSERT INTO Workout_Exercise_Template (w_id, et_id, sequence)
VALUES
  (1, 1, 1),
  (2, 2, 1),
  (3, 3, 1);

-- Insert multiple rows into Exercise_Template_Meta_Data
INSERT INTO Exercise_Template_Meta_Data (et_id, emd_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3);

INSERT INTO Recipe (user_id, title, description, calories, protein, carbs, fat)
VALUES
  (1, 'Healthy Oatmeal', 'Oatmeal with fruits', 300, 10, 50, 5),
  (1, 'Grilled Chicken', 'Chicken breast with spices', 400, 35, 0, 10),
  (1, 'Veggie Salad', 'Mixed salad with vinaigrette', 250, 5, 30, 8);

INSERT INTO Ingredients (title)
VALUES
  ('Oats'),
  ('Chicken'),
  ('Lettuce');

INSERT INTO RecipeIngredient (r_id, ing_id, amount, measurement)
VALUES
  (1, 1, 1.5, 'cup'),
  (2, 2, 2, 'pcs'),
  (3, 3, 1, 'bunch');


INSERT INTO Subscription (creator_id, subscriber_id)
VALUES
  (1, 2),
  (1, 3);


-- Insert multiple rows into Message
INSERT INTO Message (receiver_id, sender_id, content)
VALUES
  (1, 2, 'Hi, great workout!'),
  (1, 1, 'Thanks for the feedback.'),
  (1, 1, 'Welcome to my board!');

-- ========== Admin System Inserts ==========

-- Exercise_Media
INSERT INTO Exercise_Media (name, type, exercise_id)
VALUES
  ('Pushup Tutorial', 'video', 1),
  ('Running Form Image', 'image', 2),
  ('Yoga Guide Text', 'text', 3);

-- Flagged_Content
INSERT INTO Flagged_Content (reason, date_flagged, status, exercise_media, flagged_by_user, reviewed_by_admin)
VALUES
  ('Video has wrong instructions', '2025-03-28', 'pending', 1, 2, NULL),
  ('Inappropriate image', '2025-03-29', 'resolved', 2, 3, 1);

-- Activity_Log
INSERT INTO Activity_Log (timestamp, event_name, admin)
VALUES
  (NOW(), 'Flag reviewed', 1),
  (NOW(), 'Exercise media deleted', 1);

-- System_Metrics
INSERT INTO System_Metrics (timestamp, cpu_usage, memory_usage, db_latency, active_users, activity_log_id)
VALUES
  (NOW(), 47.5, 65.2, 110.4, 25, 1),
  (NOW(), 52.1, 70.3, 105.7, 30, 2);

-- Support_Tickets
INSERT INTO Support_Tickets (status, date_created, date_resolved, description, created_by_user, resolved_by_admin)
VALUES
  ('open', '2025-03-30 10:00:00', NULL, 'Media not loading', 2, NULL),
  ('closed', '2025-03-28 15:30:00', '2025-03-29 09:00:00', 'Error in log dashboard', 3, 1);

-- Demographics
INSERT INTO Demographics (demographics_id, user_id, age, gender, cultural_background, fitness_experience)
VALUES
  (1, 2, 25, 'Male', 'Asian', 'Intermediate'),
  (2, 3, 30, 'Female', 'Hispanic', 'Beginner'),
  (3, 4, 28, 'Male', 'Caucasian', 'Advanced');

-- User Demographic Data
INSERT INTO User_Demographic_Data (user_id, demographics_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3);

-- Feedback
INSERT INTO Feedback (feedback_id, user_id, survey_response, rating, comments)
VALUES
  (1, 1, 'Great experience!', 5, 'Loved the app!'),
  (2, 2, 'Needs improvement.', 3, 'UI is a bit confusing.'),
  (3, 3, 'Very useful features.', 4, 'Would recommend.');

-- User_Feedback
INSERT INTO User_Feedback (user_id, feedback_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3);

-- Sales_Report
INSERT INTO Sales_Report (report_id, date_generated, new_subscribers, cancellations, revenue_generated, roi)
VALUES
  (1, '2025-03-01', 100, 5, 5000.00, 2.5),
  (2, '2025-03-15', 150, 8, 7500.00, 3.2),
  (3, '2025-03-30', 120, 6, 6200.00, 2.8);

-- User Engagement
INSERT INTO User_Engagement (engagement_id, user_id, click_through_rate, open_rates)
VALUES
  (1, 1, 12.5, 45.3),
  (2, 2, 15.2, 50.1),
  (3, 3, 10.8, 42.7);

-- Marketing Channels
INSERT INTO Marketing_Channels (channel_id, channel_name, user_id, budget, conversions)
VALUES
  (1, 'Google Ads', 1, 5000.00, 120),
  (2, 'Facebook Ads', 2, 3000.00, 80),
  (3, 'Instagram Ads', 3, 4000.00, 95);

-- User Marketing
INSERT INTO User_Marketing (user_id, channel_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3);

-- User Engagement Marketing
INSERT INTO Users_Engagement_Marketing (engagement_id, channel_id)
VALUES
  (1, 1),
  (2, 2),
  (3, 3);

-- User Promo Code
INSERT INTO Promo_Codes (promo_code_id, user_id, discount, start_date, end_date)
VALUES
    (1, 1, 10.00, '2025-04-01', '2025-04-30'),
    (2, 3, 15.50, '2025-03-15', '2025-04-15'),
    (3, 2, 5.00, '2025-04-05', '2025-04-20'),
    (4, 4, 20.00, '2025-03-01', '2025-03-31'),
    (5, 1, 12.75, '2025-04-10', '2025-05-10');

-- App State for Maintenance

INSERT INTO App_State (setting_key, setting_value)
VALUES ('maintenance_mode', 'off');