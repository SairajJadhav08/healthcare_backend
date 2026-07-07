# Healthcare Backend

A simple Django REST API project for managing healthcare-related data such as patients, doctors, and doctor-patient assignments.

## What this project does

This backend provides basic APIs for:
- User registration and login
- Patient management
- Doctor management
- Assigning doctors to patients

## Project Structure

- accounts: user registration and login
- patients: patient-related endpoints
- doctors: doctor-related endpoints
- mappings: doctor-patient assignment endpoints

## How to run locally

1. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install the required packages
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt python-decouple psycopg2-binary
   ```

3. Set up environment variables
   Create a `.env` file with values like:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=healthcare_db
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Apply database migrations
   ```bash
   python manage.py migrate
   ```

5. Start the development server
   ```bash
   python manage.py runserver
   ```

## API Notes

- Authentication uses JWT tokens.
- The project includes a Postman collection for testing the API endpoints.

## Summary

This project was built as a practical backend system to demonstrate API development, authentication, database handling, and CRUD operations in a healthcare context.
