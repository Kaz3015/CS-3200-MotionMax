# MotionMax Project

This repository contains the codebase for the MotionMax application, a fitness and wellness platform. The project integrates a Streamlit-based frontend, a Flask REST API backend, and a MySQL database to provide a comprehensive solution for managing workouts, exercises, and recipes.

# Team Members
Julien Motaharian, Kyle Zicherman, Satvik Repaka, Joseph Grammatica

## Project Overview

The MotionMax application is designed to:
- Gives users access to created workouts from experienced trainers through a subscription.
- Allows users to track their workouts through a easy comprehensive fitness tracking solution
- Allows users to track their macronutrients and calories throughout the day through a food log
- Allows trainers to post recipes to help clients attain their dream physique.
- Messaging between a trainer and his clients is available which can be used for questions and suggestions.
- Provide role-based access control (RBAC) for different user roles (sales, trainer, clients/users, and system admin).
- Get user feedback through a posted survey and display the output to the sales administrator
- Get user demographics from the posted main user survey and display the combined user demographics to the sales administrator
- Gets the customer acquisition cost which finds the cost of acquiring a customer in a month
- Displays the customer lifetime value of the app displaying how much profit customers contribute to the app
- Get output that user inputted about their demographics and displays it to the sales admin
- Get output that user inputted about their feedback on the app and displays it to the sales admin
- Get the count of monthly subscribers we have on the app
- Get the revenue we have earned from customers on the application
- Can return a list of all the products with the sales price and the detail information for a particular product
- Can update the price of a product and mark a product out of stock
-  Get all the support tickets, submit a new support tickets, and also resolve a support
-  Get user details of a user profile by the ID, update the user profile details, remove the user account form the app
- Get the user details of a user profile by name and get current maintenance mode setting
- Can turn the maintenance mode on and off
- User can see workouts they made for themself
- User can see workouts made for them by trainers
- User can see breakdown of their workout for the day along with next up exercise information,
  muscle group information, exercise notes, technique video, and full workout exercise information
  with sets.
- User  can see a reminder to help remind them to complete their workout
- User can see motivation to get them through their next workout
- User can see their food intake per meal type
- User can see their macronutrients intake over time
- User can create themselves a new workout circuit which is completely customizable
- User can search for exercises they want to do, or create their own
- User can add as many sets as desired with multiple options to choose from
- User can include multiple exercises for the circuit, and choose the scheduled date for it
- User can add a food item to their daily food intake data based on meal type
- User can customize the food item entirely
- User can complete a set to allow for easy exercise tracking and to help them keep track of what
  they have next

## Project Structure

### 1. `app/`
This directory contains the Streamlit-based frontend for the application.

- **`src/`**: Contains the main application code.
  - **`modules/nav.py`**: Handles the sidebar navigation and role-based access control.
  - **`Home.py`**: The landing page for the application.
  - **`pages/`**: Contains pages for different user roles and functionalities.
  - **`.streamlit/config.toml`**: Configures the Streamlit app (e.g., disabling the default sidebar).

### 2. `api/`
This directory contains the Flask REST API backend.

- **`backend/`**: Contains the API routes and logic.
  - **'
  - **`customers/customer_routes.py`**: Example route for ML model predictions.
- **`.env.template`**: Template for environment variables required by the API.

### 3. `database-files/`
This directory contains SQL scripts for initializing the MySQL database.
- **`01_Trainer.sql`**: Defines the database schema for clients, including tables for workouts, exercises, food logs, and health tips.
- **`02_Trainer.sql`**: Defines the database schema for trainers, including tables for flagging content, system metrics, support tickets, and maintenance
- **`03_Admin.sql`**: Defines the database schema for systems control, including tables for, demographics, feedback, analytics for revenue, and customer aquistion cost.
- **`04_Sales.sql`**: Defines the database schema for a sales represenative, including tables for marketing channels, demographics, feedback, analytics for revenue, and customer aquistion cost.

### 4. `README.md`
Documentation for setting up and understanding the project.

## Prerequisites

- Python (Anaconda or Miniconda recommended)
- Docker and Docker Compose
- MySQL database client

### Video Link
https://www.dropbox.com/scl/fi/nkr7w1wku3lwjujknw08i/Final-motionMAX-Video.mp4?rlkey=3vlt6ygvzmfoxr38b5y9z602y&st=sklbmiu4&dl=0

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Kaz3015/CS-3200-MotionMax.git
cd <repository-folder>
run command: docker compose -f docker-compose.yaml up

