USE motionmax;

-- Exersice Media Table
INSERT INTO Exercise_Media (name, type, exercise_id)
VALUES
    ('Pushup Form Guide',          'video', 1),
    ('Proper Squat Technique',     'video', 2),
    ('Deadlift Tutorial',          'video', 3),
    ('Bench Press Basics',         'video', 4),
    ('Plank Position Guide',       'image', 5),
    ('Bicep Curl Demonstration',    'video', 6),
    ('Tricep Extension Tutorial',   'video', 7),
    ('Jumping Jack Guide',          'video', 8),
    ('Crunches Form Check',         'image', 9),
    ('Lunges Technique',            'video', 10),
    ('Pull-up Proper Form',         'video', 11),
    ('Mountain Climber Demonstration','video', 12),
    ('Burpee Step-by-Step',         'video', 13),
    ('Superman Exercise Guide',     'image', 14),
    ('Russian Twist Instructions',  'text', 15),
    ('Leg Raise Tutorial',          'video', 16),
    ('Shoulder Press Form',         'video', 17),
    ('Dumbbell Row Technique',      'video', 18),
    ('Calf Raise Basics',           'image', 19),
    ('Glute Bridge Guide',          'text', 20),
    ('Lat Pulldown Tutorial',       'video', 21),
    ('Chest Fly Demonstration',     'video', 22),
    ('Side Plank Position',         'image', 23),
    ('Hip Thrust Form Check',       'video', 24),
    ('Box Jump Technique',          'video', 25),
    ('Kettlebell Swing Guide',      'video', 26),
    ('Overhead Squat Tutorial',     'video', 27),
    ('Face Pull Instructions',      'text', 28),
    ('Reverse Crunch Guide',        'image', 29),
    ('Battle Rope Workout',         'video', 30),
    ('Elliptical Machine Guide',    'text', 31),
    ('Treadmill Basics',            'video', 32),
    ('Rowing Machine Form',         'video', 33),
    ('Stair Climber Tutorial',      'text', 34),
    ('Leg Press Demonstration',     'video', 35),
    ('Seated Row Guide',            'video', 36),
    ('Cable Crossover Form',        'image', 37),
    ('Leg Extension Technique',     'video', 38),
    ('Hamstring Curl Tutorial',     'video', 39),
    ('Ab Roller Guide',             'video', 40),
    ('Medicine Ball Slam',          'video', 41),
    ('Resistance Band Exercises',   'text', 42),
    ('TRX Row Form Check',          'image', 43),
    ('Barbell Hip Thrust',          'video', 44),
    ('Landmine Press Guide',        'video', 45),
    ('Cable Woodchop Technique',    'video', 46),
    ('Dumbbell Pullover Tutorial',  'image', 47),
    ('Nordic Hamstring Curl',       'video', 48),
    ('Swiss Ball Crunch Guide',     'text', 49),
    ('Hanging Leg Raise Form',      'video', 50);


INSERT INTO Flagged_Content (
  reason,
  date_flagged,
  status,
  exercise_media,
  flagged_by_user,
  reviewed_by_admin
) VALUES
    ('Incorrect form shown in video',            '2025-01-15', 'resolved', 1,  5,  1),
    ('Inappropriate content in background',       '2025-01-18', 'dismissed',3,  8,  2),
    ('Potentially dangerous technique',           '2025-01-22', 'resolved', 7, 12, 1),
    ('Outdated exercise recommendation',          '2025-01-25', 'pending',  10, 7,  NULL),
    ('Audio quality issues',                      '2025-01-28', 'resolved', 12, 15, 3),
    ('Missing crucial safety information',        '2025-02-01', 'resolved', 15, 6,  1),
    ('Exercise not suitable for beginners',       '2025-02-03', 'dismissed',18, 9,  2),
    ('Misleading thumbnail',                      '2025-02-05', 'pending',  22, 14, NULL),
    ('Contains advertisement',                    '2025-02-08', 'resolved', 25, 20, 4),
    ('Poor lighting makes form difficult to see', '2025-02-10', 'pending',  28, 11, NULL),
    ('Contradicts other tutorial materials',      '2025-02-12', 'resolved', 30, 17, 1),
    ('Broken video link',                         '2025-02-15', 'resolved', 32, 23, 2),
    ('Text contains typos',                       '2025-02-18', 'dismissed',34, 16, 3),
    ('Exercise could cause injury',               '2025-02-20', 'resolved', 37, 19, 1),
    ('Music too loud compared to instruction',    '2025-02-22', 'pending',  39, 25, NULL),
    ('Instructor uses confusing terminology',     '2025-02-25', 'dismissed',41, 13, 4),
    ('Image quality too low',                     '2025-02-28', 'resolved', 43, 22, 2),
    ('Wrong muscle group identified',             '2025-03-02', 'pending',  45, 27, NULL),
    ('Duplicate of existing content',             '2025-03-05', 'resolved', 48, 18, 1),
    ('Content not accessible for disabled users', '2025-03-07', 'pending',  50, 24, NULL);
    
INSERT INTO Activity_Log (timestamp, event_name, admin)
VALUES
    ('2025-01-01 09:15:23', 'User account suspended', 1),
    ('2025-01-01 10:32:44', 'Exercise media approved', 2),
    ('2025-01-01 13:45:12', 'Flag resolved', 3),
    ('2025-01-01 15:22:37', 'New category created', 1),
    ('2025-01-02 08:30:15', 'Exercise media rejected', 4),
    ('2025-01-02 11:17:39', 'User banned', 2),
    ('2025-01-02 14:05:28', 'Flag dismissed', 1),
    ('2025-01-03 09:45:33', 'Bulk content approval', 3),
    ('2025-01-03 12:12:54', 'System settings updated', 2),
    ('2025-01-03 16:30:22', 'Exercise program reviewed', 4),
    ('2025-01-04 08:55:17', 'User warning issued', 1),
    ('2025-01-04 11:40:39', 'Content removed', 3),
    ('2025-01-04 15:22:48', 'Backup performed', 2),
    ('2025-01-05 09:10:25', 'Comment deleted', 4),
    ('2025-01-05 13:05:11', 'Access permission modified', 1),
    ('2025-01-06 08:20:33', 'Spam content removed', 3),
    ('2025-01-06 11:45:59', 'Forum post moderated', 2),
    ('2025-01-06 15:30:12', 'User account restored', 4),
    ('2025-01-07 09:25:45', 'Security alert addressed', 1),
    ('2025-01-07 12:15:32', 'Database maintenance', 3),
    ('2025-01-07 16:40:18', 'API access revoked', 2),
    ('2025-01-08 08:35:27', 'Content migration', 4),
    ('2025-01-08 11:50:43', 'Instructor approval', 1),
    ('2025-01-08 14:25:16', 'Review request processed', 3),
    ('2025-01-09 09:30:38', 'Analytics report generated', 2),
    ('2025-01-09 12:20:54', 'Payment dispute resolved', 4),
    ('2025-01-09 15:45:22', 'Promotional content approved', 1),
    ('2025-01-10 08:15:49', 'Video quality review', 3),
    ('2025-01-10 11:35:27', 'User group created', 2),
    ('2025-01-10 14:50:36', 'Content featured on homepage', 4),
    ('2025-01-11 09:05:43', 'System alert investigated', 1),
    ('2025-01-11 12:30:19', 'Bulk user import', 3),
    ('2025-01-11 15:55:28', 'Category reorganization', 2),
    ('2025-01-12 08:40:37', 'Exercise description updated', 4),
    ('2025-01-12 11:25:53', 'Payment method added', 1),
    ('2025-01-12 14:10:16', 'Database query optimization', 3),
    ('2025-01-13 09:35:42', 'Content accessibility review', 2),
    ('2025-01-13 12:50:26', 'Challenge program approved', 4),
    ('2025-01-13 16:15:33', 'Newsletter drafted', 1),
    ('2025-01-14 08:25:19', 'A/B test initiated', 3),
    ('2025-01-14 11:45:38', 'Notification template updated', 2),
    ('2025-01-14 15:05:27', 'Exercise progression reviewed', 4),
    ('2025-01-15 09:20:44', 'Login anomaly investigated', 1),
    ('2025-01-15 12:40:13', 'Instructor verification', 3),
    ('2025-01-15 16:30:29', 'Community guidelines updated', 2),
    ('2025-01-16 08:30:52', 'Certification process approved', 4),
    ('2025-01-16 11:55:18', 'Content rating system adjusted', 1),
    ('2025-01-16 14:15:37', 'Password reset audit', 3),
    ('2025-01-17 09:40:26', 'Feature rollout approved', 2),
    ('2025-01-17 12:25:49', 'User feedback processed', 4),
    ('2025-01-17 15:50:33', 'Affiliate program reviewed', 1),
    ('2025-01-18 08:10:15', 'Security patch applied', 3),
    ('2025-01-18 11:30:48', 'Content verification process', 2),
    ('2025-01-18 14:55:22', 'Membership tier adjusted', 4),
    ('2025-01-19 09:15:37', 'Scheduled maintenance', 1),
    ('2025-01-19 12:35:54', 'Data export request processed', 3),
    ('2025-01-19 16:20:19', 'Social media integration updated', 2),
    ('2025-01-20 08:45:28', 'Discount code approved', 4),
    ('2025-01-20 11:20:43', 'Privacy policy update reviewed', 1),
    ('2025-01-20 14:40:16', 'Content recommendation adjustment', 3),
    ('2025-01-21 09:05:32', 'SSL certificate renewed', 2),
    ('2025-01-21 12:15:49', 'Exercise video transcribed', 4),
    ('2025-01-21 15:35:27', 'Push notification approved', 1),
    ('2025-01-22 08:55:18', 'Cache cleared', 3),
    ('2025-01-22 11:40:36', 'Custom report generated', 2),
    ('2025-01-22 14:25:54', 'Progress tracking feature updated', 4),
    ('2025-01-23 09:30:17', 'Emergency downtime initiated', 1),
    ('2025-01-23 12:50:35', 'Automated email sequence reviewed', 3),
    ('2025-01-23 16:10:28', 'User permission audit', 2),
    ('2025-01-24 08:20:46', 'Language translation approved', 4),
    ('2025-01-24 11:15:33', 'Billing system update', 1),
    ('2025-01-24 14:45:19', 'Content age restriction applied', 3),
    ('2025-01-25 09:25:28', 'Workout template approved', 2),
    ('2025-01-25 12:05:47', 'User challenge created', 4),
    ('2025-01-25 15:40:36', 'Error logs reviewed', 1),
    ('2025-01-26 08:50:23', 'Email deliverability issue resolved', 3),
    ('2025-01-26 11:35:42', 'Content tagging system updated', 2),
    ('2025-01-26 14:20:15', 'User achievement created', 4),
    ('2025-01-27 09:00:38', 'Seasonal promotion approved', 1),
    ('2025-01-27 12:45:27', 'User engagement report generated', 3),
    ('2025-01-27 16:05:53', 'Exercise equipment list updated', 2),
    ('2025-01-28 08:15:16', 'Third-party integration review', 4),
    ('2025-01-28 11:50:34', 'Server performance optimization', 1),
    ('2025-01-28 14:30:22', 'Exercise difficulty adjusted', 3),
    ('2025-01-29 09:10:45', 'Subscription plan modified', 2),
    ('2025-01-29 12:55:18', 'Content scheduling approved', 4),
    ('2025-01-29 15:25:37', 'DDoS protection updated', 1),
    ('2025-01-30 08:40:26', 'User survey created', 3),
    ('2025-01-30 11:05:49', 'Payment gateway update', 2),
    ('2025-01-30 14:50:32', 'Trainer certification verified', 4),
    ('2025-01-31 09:20:17', 'API documentation updated', 1),
    ('2025-01-31 12:00:38', 'Bulk content tags updated', 3),
    ('2025-01-31 15:30:54', 'Feature deprecation scheduled', 2),
    ('2025-02-01 08:35:23', 'User role restructured', 4),
    ('2025-02-01 11:25:47', 'Content export completed', 1),
    ('2025-02-01 14:15:36', 'System notification approved', 3),
    ('2025-02-02 09:45:28', 'Audit log review', 2),
    ('2025-02-02 12:10:43', 'User merge performed', 4),
    ('2025-02-02 15:50:19', 'App update reviewed', 1),
    ('2025-02-03 08:00:34', 'Batch content processing', 3),
    ('2025-02-03 11:30:52', 'Email template updated', 2),
    ('2025-02-03 14:55:15', 'Forum category restructured', 4),
    ('2025-02-04 09:35:28', 'Database index optimization', 1),
    ('2025-02-04 12:20:47', 'User onboarding flow updated', 3),
    ('2025-02-04 16:00:33', 'Content duplication review', 2),
    ('2025-02-05 08:25:16', 'Fitness challenge approved', 4),
    ('2025-02-05 11:55:39', 'Critical error resolved', 1),
    ('2025-02-05 14:35:28', 'Content search algorithm adjusted', 3),
    ('2025-02-06 09:15:43', 'User data export processed', 2),
    ('2025-02-06 12:30:19', 'Featured trainer approved', 4),
    ('2025-02-06 15:45:36', 'Database backup verified', 1),
    ('2025-02-07 08:05:27', 'New payment method enabled', 3),
    ('2025-02-07 11:40:58', 'Global settings adjusted', 2),
    ('2025-02-07 14:10:23', 'Workout template verified', 4),
    ('2025-02-08 09:50:34', 'Content metadata updated', 1),
    ('2025-02-08 12:15:49', 'User reported issue resolved', 3),
    ('2025-02-08 15:55:28', 'API rate limit adjusted', 2),
    ('2025-02-09 08:30:17', 'User milestone created', 4),
    ('2025-02-09 11:10:46', 'Load balancer configuration', 1),
    ('2025-02-09 14:40:33', 'Content approval guidelines updated', 3),
    ('2025-02-10 09:00:22', 'Mobile app configuration update', 2),
    ('2025-02-10 12:45:38', 'Exercise sequence approved', 4);

INSERT INTO System_Metrics (timestamp, cpu_usage, memory_usage, db_latency, active_users, activity_log_id)
VALUES
    ('2025-01-01 09:15:23', 45.8, 62.3, 98.7, 120, 1),
    ('2025-01-01 10:32:44', 48.2, 65.7, 105.3, 145, 2),
    ('2025-01-01 13:45:12', 52.6, 68.9, 110.2, 178, 3),
    ('2025-01-01 15:22:37', 57.3, 72.1, 112.5, 203, 4),
    ('2025-01-02 08:30:15', 43.5, 60.8, 95.4, 112, 5),
    ('2025-01-02 11:17:39', 47.9, 63.5, 99.8, 156, 6),
    ('2025-01-02 14:05:28', 54.2, 67.3, 107.6, 187, 7),
    ('2025-01-03 09:45:33', 42.1, 59.6, 92.3, 108, 8),
    ('2025-01-03 12:12:54', 45.7, 62.8, 97.5, 143, 9),
    ('2025-01-03 16:30:22', 51.3, 68.2, 103.9, 172, 10),
    ('2025-01-04 08:55:17', 41.8, 58.7, 91.2, 98, 11),
    ('2025-01-04 11:40:39', 44.6, 61.9, 96.8, 132, 12),
    ('2025-01-04 15:22:48', 49.5, 65.3, 101.7, 165, 13),
    ('2025-01-05 09:10:25', 40.9, 57.8, 90.6, 92, 14),
    ('2025-01-05 13:05:11', 44.3, 60.2, 95.3, 128, 15),
    ('2025-01-06 08:20:33', 42.7, 58.1, 92.9, 105, 16),
    ('2025-01-06 11:45:59', 46.8, 62.5, 98.2, 138, 17),
    ('2025-01-06 15:30:12', 51.9, 67.8, 104.7, 179, 18),
    ('2025-01-07 09:25:45', 43.2, 59.3, 93.8, 110, 19),
    ('2025-01-07 12:15:32', 48.5, 63.7, 100.5, 145, 20),
    ('2025-01-07 16:40:18', 54.7, 69.2, 108.3, 192, 21),
    ('2025-01-08 08:35:27', 42.5, 58.9, 92.1, 103, 22),
    ('2025-01-08 11:50:43', 46.3, 62.1, 97.6, 136, 23),
    ('2025-01-08 14:25:16', 50.8, 67.4, 103.2, 172, 24),
    ('2025-01-09 09:30:38', 44.7, 60.5, 95.9, 115, 25),
    ('2025-01-09 12:20:54', 49.3, 65.8, 102.1, 150, 26),
    ('2025-01-09 15:45:22', 55.1, 70.3, 109.8, 195, 27),
    ('2025-01-10 08:15:49', 43.8, 59.7, 94.2, 111, 28),
    ('2025-01-10 11:35:27', 47.6, 63.9, 99.5, 142, 29),
    ('2025-01-10 14:50:36', 52.9, 68.7, 106.3, 183, 30),
    ('2025-01-11 09:05:43', 42.3, 58.5, 91.7, 102, 31),
    ('2025-01-11 12:30:19', 46.9, 62.7, 98.3, 139, 32),
    ('2025-01-11 15:55:28', 53.5, 69.4, 107.9, 189, 33),
    ('2025-01-12 08:40:37', 41.5, 57.6, 90.8, 95, 34),
    ('2025-01-12 11:25:53', 45.2, 61.3, 96.2, 130, 35),
    ('2025-01-12 14:10:16', 50.4, 66.8, 102.5, 168, 36),
    ('2025-01-13 09:35:42', 43.6, 59.2, 93.4, 107, 37),
    ('2025-01-13 12:50:26', 48.1, 64.5, 100.9, 148, 38),
    ('2025-01-13 16:15:33', 54.3, 70.1, 108.7, 190, 39),
    ('2025-01-14 08:25:19', 42.9, 58.3, 92.5, 104, 40),
    ('2025-01-14 11:45:38', 47.3, 63.1, 98.9, 140, 41),
    ('2025-01-14 15:05:27', 53.1, 68.6, 106.8, 185, 42),
    ('2025-01-15 09:20:44', 44.5, 60.8, 95.1, 113, 43),
    ('2025-01-15 12:40:13', 48.7, 65.2, 101.3, 152, 44),
    ('2025-01-15 16:30:29', 55.4, 71.5, 110.6, 198, 45),
    ('2025-01-16 08:30:52', 43.9, 59.5, 94.7, 109, 46),
    ('2025-01-16 11:55:18', 47.5, 63.4, 99.1, 144, 47),
    ('2025-01-16 14:15:37', 52.7, 68.2, 105.8, 180, 48),
    ('2025-01-17 09:40:26', 45.1, 61.2, 96.4, 118, 49),
    ('2025-01-17 12:25:49', 49.6, 65.9, 102.7, 156, 50),
    ('2025-01-17 15:50:33', 56.2, 72.3, 111.9, 202, 51),
    ('2025-01-18 08:10:15', 44.2, 60.1, 93.5, 106, 52),
    ('2025-01-18 11:30:48', 48.4, 64.3, 100.2, 146, 53),
    ('2025-01-18 14:55:22', 53.8, 69.7, 107.4, 187, 54),
    ('2025-01-19 09:15:37', 43.5, 59.8, 92.7, 105, 55),
    ('2025-01-19 12:35:54', 47.8, 63.6, 98.5, 141, 56),
    ('2025-01-19 16:20:19', 54.6, 70.5, 109.3, 193, 57),
    ('2025-01-20 08:45:28', 42.6, 58.4, 91.3, 99, 58),
    ('2025-01-20 11:20:43', 46.5, 62.2, 97.1, 133, 59),
    ('2025-01-20 14:40:16', 51.1, 67.6, 104.5, 175, 60),
    ('2025-01-21 09:05:32', 44.9, 61.4, 96.7, 119, 61),
    ('2025-01-21 12:15:49', 49.2, 65.1, 101.9, 154, 62),
    ('2025-01-21 15:35:27', 55.7, 71.8, 111.2, 200, 63),
    ('2025-01-22 08:55:18', 43.3, 59.1, 93.1, 108, 64),
    ('2025-01-22 11:40:36', 48.1, 64.8, 100.7, 145, 65),
    ('2025-01-22 14:25:54', 53.4, 69.5, 107.1, 184, 66),
    ('2025-01-23 09:30:17', 45.3, 61.7, 97.4, 120, 67),
    ('2025-01-23 12:50:35', 50.1, 66.3, 103.5, 160, 68),
    ('2025-01-23 16:10:28', 56.5, 72.7, 112.8, 205, 69),
    ('2025-01-24 08:20:46', 44.1, 60.3, 94.3, 112, 70),
    ('2025-01-24 11:15:33', 48.8, 64.1, 99.6, 147, 71),
    ('2025-01-24 14:45:19', 53.9, 70.2, 108.5, 188, 72),
    ('2025-01-25 09:25:28', 45.6, 61.9, 98.1, 123, 73),
    ('2025-01-25 12:05:47', 49.7, 66.4, 102.3, 158, 74),
    ('2025-01-25 15:40:36', 55.9, 71.9, 111.5, 201, 75),
    ('2025-01-26 08:50:23', 43.7, 59.9, 94.9, 114, 76),
    ('2025-01-26 11:35:42', 47.4, 63.8, 99.3, 143, 77),
    ('2025-01-26 14:20:15', 52.5, 68.1, 106.1, 179, 78),
    ('2025-01-27 09:00:38', 44.4, 60.6, 95.5, 116, 79),
    ('2025-01-27 12:45:27', 48.9, 65.4, 101.2, 151, 80),
    ('2025-01-27 16:05:53', 54.4, 70.7, 109.6, 194, 81),
    ('2025-01-28 08:15:16', 43.4, 58.7, 92.3, 107, 82),
    ('2025-01-28 11:50:34', 47.1, 62.9, 97.8, 137, 83),
    ('2025-01-28 14:30:22', 51.6, 67.3, 104.2, 174, 84),
    ('2025-01-29 09:10:45', 45.2, 61.1, 96.1, 117, 85),
    ('2025-01-29 12:55:18', 49.9, 65.6, 102.9, 155, 86),
    ('2025-01-29 15:25:37', 55.3, 71.2, 110.8, 196, 87),
    ('2025-01-30 08:40:26', 42.8, 58.2, 91.5, 101, 88),
    ('2025-01-30 11:05:49', 47.6, 63.3, 98.7, 138, 89),
    ('2025-01-30 14:50:32', 52.3, 68.5, 105.4, 177, 90),
    ('2025-01-31 09:20:17', 44.8, 60.9, 95.7, 115, 91),
    ('2025-01-31 12:00:38', 49.1, 65.2, 101.6, 153, 92),
    ('2025-01-31 15:30:54', 54.8, 70.9, 110.1, 197, 93),
    ('2025-02-01 08:35:23', 43.2, 58.6, 92.8, 103, 94),
    ('2025-02-01 11:25:47', 47.9, 63.7, 99.4, 142, 95),
    ('2025-02-01 14:15:36', 53.7, 69.3, 107.7, 186, 96),
    ('2025-02-02 09:45:28', 45.5, 61.6, 97.3, 121, 97),
    ('2025-02-02 12:10:43', 50.3, 66.5, 103.1, 161, 98),
    ('2025-02-02 15:50:19', 57.1, 73.2, 113.4, 209, 99),
    ('2025-02-03 08:00:34', 44.3, 60.4, 94.5, 113, 100),
    ('2025-02-03 11:30:52', 48.5, 64.2, 99.9, 148, 101),
    ('2025-02-03 14:55:15', 53.2, 68.9, 106.5, 181, 102),
    ('2025-02-04 09:35:28', 45.9, 62.1, 98.5, 124, 103),
    ('2025-02-04 12:20:47', 50.6, 66.7, 103.8, 163, 104),
    ('2025-02-04 16:00:33', 56.4, 72.5, 112.2, 204, 105),
    ('2025-02-05 08:25:16', 43.6, 59.4, 93.3, 109, 106),
    ('2025-02-05 11:55:39', 47.2, 63.0, 98.1, 139, 107),
    ('2025-02-05 14:35:28', 51.5, 67.9, 105.1, 176, 108),
    ('2025-02-06 09:15:43', 45.1, 61.3, 96.5, 118, 109),
    ('2025-02-06 12:30:19', 49.5, 65.0, 102.4, 157, 110),
    ('2025-02-06 15:45:36', 55.6, 71.4, 111.3, 199, 111),
    ('2025-02-07 08:05:27', 42.4, 58.0, 91.1, 97, 112),
    ('2025-02-07 11:40:58', 46.7, 62.4, 97.9, 135, 113),
    ('2025-02-07 14:10:23', 51.8, 67.1, 104.8, 173, 114),
    ('2025-02-08 09:50:34', 44.6, 60.7, 95.6, 114, 115),
    ('2025-02-08 12:15:49', 48.3, 64.6, 100.3, 149, 116);

INSERT INTO Support_Tickets (
  status,
  date_created,
  date_resolved,
  description,
  created_by_user,
  resolved_by_admin
) VALUES
    ('open',        '2025-01-01 08:32:17', NULL, 'Unable to upload exercise videos',               3,  NULL),
    ('closed',      '2025-01-01 09:45:23', '2025-01-01 14:30:12', 'Login issues after password reset',     5,   1),
    ('in_progress', '2025-01-01 11:20:45', NULL, 'Exercise tracking not recording properly',     8,   2),
    ('closed',      '2025-01-01 13:55:32', '2025-01-02 10:15:47', 'Billing error on subscription renewal',  12,  1),
    ('open',        '2025-01-02 09:10:28', NULL, 'Video playback freezing midway',            7,  NULL),
    ('closed',      '2025-01-02 10:35:19', '2025-01-02 15:40:53', 'Unable to update profile picture',       14,  3),
    ('in_progress', '2025-01-02 12:15:43', NULL, 'Exercise program not showing all exercises', 9,   2),
    ('closed',      '2025-01-02 14:50:36', '2025-01-03 09:25:18', 'Incorrect exercise descriptions',         18,  4),
    ('open',        '2025-01-03 08:25:51', NULL, 'App crashing during workout timer',        6,  NULL),
    ('closed',      '2025-01-03 10:15:27', '2025-01-03 16:35:42', 'Cannot connect fitness tracker',         15,  1),
    ('in_progress', '2025-01-03 11:55:38', NULL, 'Nutrition tracking showing wrong calories',11,  3),
    ('closed',      '2025-01-03 14:30:21', '2025-01-04 11:20:35', 'Payment method declined but account charged',20, 2),
    ('open',        '2025-01-04 09:45:12', NULL, 'Video resolution quality issues',         4,  NULL),
    ('closed',      '2025-01-04 11:20:34', '2025-01-04 17:15:29', 'Cannot access downloaded workout plans',17,  4),
    ('in_progress', '2025-01-04 13:05:48', NULL, 'Progress charts not updating',             10, 1),
    ('closed',      '2025-01-04 15:40:23', '2025-01-05 10:30:17', 'Exercise media showing incorrect thumbnails',22,3),
    ('open',        '2025-01-05 08:15:36', NULL, 'Unable to share workouts with friends',     5,  NULL),
    ('closed',      '2025-01-05 10:50:28', '2025-01-05 15:25:43', 'Email notifications not being received',  19, 2),
    ('in_progress', '2025-01-05 12:30:15', NULL, 'Workout timer stopping randomly',          13, 4),
    ('closed',      '2025-01-05 15:10:42', '2025-01-06 09:45:31', 'Exercise search returning irrelevant results',24,1),
    ('open',        '2025-01-06 09:35:27', NULL, 'Unable to sync across devices',             8,  NULL),
    ('closed',      '2025-01-06 11:15:39', '2025-01-06 16:50:24', 'Calendar scheduling not working',         21, 3),
    ('in_progress', '2025-01-06 13:45:52', NULL, 'Account preferences not saving',           16, 2),
    ('closed',      '2025-01-06 16:20:18', '2025-01-07 11:10:35', 'Incorrect muscle group targeting in filter',25,4),
    ('open',        '2025-01-07 08:50:43', NULL, 'Exercise media not loading on mobile',      7,  NULL),
    ('closed',      '2025-01-07 10:25:31', '2025-01-07 15:30:46', 'Password reset email not receiving',      23, 1),
    ('in_progress', '2025-01-07 12:55:19', NULL, 'Workout plan generator not working',       14, 3),
    ('closed',      '2025-01-07 15:30:47', '2025-01-08 10:15:33', 'Unable to cancel subscription',           27, 2),
    ('open',        '2025-01-08 09:10:25', NULL, 'Exercise difficulty ratings incorrect',    9,  NULL),
    ('closed',      '2025-01-08 11:45:38', '2025-01-08 17:20:12', 'Account locked after multiple login attempts',26,4),
    ('in_progress', '2025-01-08 14:15:56', NULL, 'Unable to log cardio exercises properly',  18, 1),
    ('closed',      '2025-01-08 16:50:23', '2025-01-09 12:35:42', 'Exercise history shows duplicate entries',29,3),
    ('open',        '2025-01-09 08:30:14', NULL, 'Media streaming buffering constantly',      12, NULL),
    ('closed',      '2025-01-09 10:55:37', '2025-01-09 16:10:28', 'Cannot edit saved workout routines',      28,2),
    ('in_progress', '2025-01-09 13:25:49', NULL, 'Goal tracking system not updating',        15,4),
    ('closed',      '2025-01-09 16:05:32', '2025-01-10 11:45:18', 'Exercise timer counting incorrectly',     31,1),
    ('open',        '2025-01-10 09:20:45', NULL, 'Unable to invite friends to challenge',    11, NULL),
    ('closed',      '2025-01-10 11:40:51', '2025-01-10 17:15:35', 'Certification badge not displaying',      30,3),
    ('in_progress', '2025-01-10 14:15:27', NULL, 'Exercise form tips not showing',           19,2),
    ('closed',      '2025-01-10 16:45:36', '2025-01-11 12:30:24', 'Incorrect exercise equipment listed',    33,4),
    ('open',        '2025-01-11 08:55:18', NULL, 'Cannot generate PDF workout plan',         16, NULL),
    ('closed',      '2025-01-11 11:25:29', '2025-01-11 16:40:17', 'Profile achievements not updating',      32,1),
    ('in_progress', '2025-01-11 13:50:43', NULL, 'Exercise video playback stuttering',       21,3),
    ('closed',      '2025-01-11 16:30:15', '2025-01-12 10:15:38', 'Nutrition tracker not accepting custom foods',35,2),
    ('open',        '2025-01-12 09:15:27', NULL, 'Exercise demonstration videos broken',     13, NULL),
    ('closed',      '2025-01-12 11:50:39', '2025-01-12 17:25:46', 'Cannot reset workout progress',          34,4),
    ('in_progress', '2025-01-12 14:25:52', NULL, 'Heart rate monitor integration failing',   24,1),
    ('closed',      '2025-01-12 16:55:33', '2025-01-13 12:40:21', 'Exercise media showing wrong muscle groups',37,3),
    ('open',        '2025-01-13 08:35:46', NULL, 'Workout plan builder not saving changes',  17, NULL),
    ('closed',      '2025-01-13 11:10:28', '2025-01-13 16:35:53', 'Cannot modify account settings',         36,2),
    ('in_progress', '2025-01-13 13:45:37', NULL, 'Exercise search filter not working',      25,4),
    ('closed',      '2025-01-13 16:20:15', '2025-01-14 11:05:29', 'Incorrect calories burned calculation',  39,1),
    ('open',        '2025-01-14 09:40:23', NULL, 'Unable to access premium content',        20, NULL),
    ('closed',      '2025-01-14 12:15:36', '2025-01-14 17:50:42', 'Account email change verification not working',38,3),
    ('in_progress', '2025-01-14 14:50:52', NULL, 'Exercise progression suggestions incorrect',27,2),
    ('closed',      '2025-01-14 17:25:18', '2025-01-15 13:10:34', 'Subscription renewal notification not received',41,4),
    ('open',        '2025-01-15 08:45:33', NULL, 'Exercise video commentary inaudible',      22, NULL),
    ('closed',      '2025-01-15 11:20:45', '2025-01-15 16:55:38', 'Unable to update payment information',   40,1),
    ('in_progress', '2025-01-15 14:05:27', NULL, 'Exercise playlist creating duplicates',    29,3),
    ('closed',      '2025-01-15 16:40:36', '2025-01-16 12:25:19', 'Progress photos not saving',             43,2),
    ('open',        '2025-01-16 09:25:51', NULL, 'Exercise timer audio alerts not working',23, NULL),
    ('closed',      '2025-01-16 12:10:29', '2025-01-16 17:35:47', 'Cannot connect to Bluetooth devices',    42,4),
    ('in_progress', '2025-01-16 14:35:14', NULL, 'Exercise notes feature not saving',       31,1),
    ('closed',      '2025-01-16 17:15:42', '2025-01-17 11:50:23', 'Incorrect billing amount',               45,3),
    ('open',        '2025-01-17 08:40:17', NULL, 'Workout rest timer not functioning',      26, NULL),
    ('closed',      '2025-01-17 11:15:36', '2025-01-17 16:40:52', 'Exercise video speed controls not working',44,2),
    ('in_progress', '2025-01-17 14:45:28', NULL, 'Cannot update height/weight metrics',     33,4),
    ('closed',      '2025-01-17 17:20:15', '2025-01-18 12:05:37', 'Exercise media showing incorrect duration',47,1),
    ('open',        '2025-01-18 09:50:33', NULL, 'Unable to export workout history',       28, NULL),
    ('closed',      '2025-01-18 12:25:45', '2025-01-18 17:50:19', 'Exercise media subtitles missing',       46,3),
    ('in_progress', '2025-01-18 15:10:27', NULL, 'Weight tracking graph not displaying',    35,2),
    ('closed',      '2025-01-18 17:45:39', '2025-01-19 13:30:28', 'Exercise favorites feature not working',49,4),
    ('open',        '2025-01-19 08:15:52', NULL, 'Unable to submit feedback forms',         30, NULL),
    ('closed',      '2025-01-19 11:40:18', '2025-01-19 16:15:33', 'Personal records not updating',          48,1),
    ('in_progress', '2025-01-19 14:25:35', NULL, 'Exercise media search not finding keywords',37,3),
    ('closed',      '2025-01-19 16:55:29', '2025-01-20 11:40:48', 'Unable to update notification preferences', 1,2),
    ('open',        '2025-01-20 09:30:41', NULL, 'Exercise video quality selection not working',32, NULL),
    ('closed',      '2025-01-20 12:05:23', '2025-01-20 17:30:35', 'Cannot reset password',                   49,4),
    ('in_progress', '2025-01-20 14:50:37', NULL, 'Exercise recommendations not relevant',   39,1),
    ('closed',      '2025-01-20 17:25:19', '2025-01-21 12:10:42', 'Workout schedule calendar errors',         3,3),
    ('open',        '2025-01-21 08:55:28', NULL, 'Exercise voice commands not working',     34, NULL),
    ('closed',      '2025-01-21 11:30:36', '2025-01-21 16:55:23', 'Subscription benefits not accessible',     2,2),
    ('in_progress', '2025-01-21 14:15:42', NULL, 'Exercise comparison feature broken',       41,4),
    ('closed',      '2025-01-21 16:50:15', '2025-01-22 11:25:37', 'Unable to view workout history',           5,1),
    ('open',        '2025-01-22 09:20:33', NULL, 'Exercise media downloading error',        36, NULL),
    ('closed',      '2025-01-22 12:45:27', '2025-01-22 17:20:19', 'Unable to view completed workouts',       4,3),
    ('in_progress', '2025-01-22 15:30:36', NULL, 'Exercise timer notification not triggering',43,2),
    ('closed',      '2025-01-22 18:05:42', '2025-01-23 12:50:28', 'Workout intensity calculation incorrect',  7,4),
    ('open',        '2025-01-23 08:40:19', NULL, 'Exercise video bookmarking not working',  38, NULL),
    ('closed',      '2025-01-23 11:15:36', '2025-01-23 16:40:52', 'Profile statistics displaying wrong data', 6,1),
    ('in_progress', '2025-01-23 14:50:28', NULL, 'Exercise category filter not applying',    45,3),
    ('closed',      '2025-01-23 17:25:15', '2025-01-24 13:10:37', 'Workout routine not saving changes',      9,2),
    ('open',        '2025-01-24 09:05:33', NULL, 'Exercise instruction text missing',       40, NULL),
    ('closed',      '2025-01-24 12:35:18', '2025-01-24 17:50:45', 'Cannot cancel recurring subscription',    8,4),
    ('in_progress', '2025-01-24 15:15:42', NULL, 'Exercise media not filtered by equipment',47,1),
    ('closed',      '2025-01-24 17:50:26', '2025-01-25 11:35:19', 'Workout reminder notifications not working',11,3);


--  App State for Maintenance

INSERT INTO App_State (setting_key, setting_value)
VALUES ('maintenance_mode', 'off');