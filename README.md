# MotionMax Project

This repository contains the codebase for the MotionMax application, a fitness and wellness platform. The project integrates a Streamlit-based frontend, a Flask REST API backend, and a MySQL database to provide a comprehensive solution for managing workouts, exercises, and recipes.

## Project Overview

The MotionMax application is designed to:
- Gives users access to created workouts from experienced trainers through a subscription.
- Allows users to track their workouts through a easy comprehensive fitness tracking soluton
- Allows users to track their macronurteitns and calories throughout the day through a food log
- Allows trainers to post recipes to help clients attain their dream physique.
- Messaging between a trainer and his clients is avaivbile which can be used for questions and suggestions.
- Provide role-based access control (RBAC) for different user roles (sales, trainer, clients/users, and system admin.

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

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Kaz3015/CS-3200-MotionMax.git
cd <repository-folder>
run command: docker compose -f docker-compose.yaml up 
