# Inventory Management System API

This project implements an Inventory Management System using Django Rest Framework. It supports CRUD operations on inventory items and includes JWT-based authentication for secure access.

## Table of Contents
- [Project Setup](#project-setup)
- [API Documentation](#api-documentation)
- [Requirements](#requirements)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Testing](#testing)

## Project Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/darshan-06/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root and add your database configurations:
   ```plaintext
   DATABASE_NAME=db_name
   DATABASE_USER=db_user
   DATABASE_PASSWORD=db_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   SECRET_KEY=secret_key
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## API Documentation

### User Registration
- **Endpoint:** `/register/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "newuser",
      "password": "newpassword"
  }
  ```
- **Response:**
  - Status: `201 Created`

### Token Generation
- **Endpoint:** `/token/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "username": "testuser",
      "password": "password"
  }
  ```
- **Response:**
  - Status: `200 OK`
  - Body:
  ```json
  {
      "access": "access_token",
      "refresh": "refresh_token"
  }
  ```

### Refresh Token
- **Endpoint:** `/token/refresh/`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
      "refresh": "refresh_token"
  }
  ```
- **Response:**
  - Status: `200 OK`
  - Body:
  ```json
  {
      "access": "new_access_token"
  }
  ```

### CRUD Operations for Items
1. **Create Item**
   - **Endpoint:** `/items/`
   - **Method:** `POST`
   - **Request Body:**
   ```json
   {
       "name": "New Item",
       "quantity": 5,
       "price": 50.00
   }
   ```
   - **Response:**
     - Status: `201 Created`

2. **Get Item**
   - **Endpoint:** `/items/<int:item_id>/`
   - **Method:** `GET`
   - **Response:**
     - Status: `200 OK`
     - Body:
     ```json
     {
         "id": 1,
         "name": "Test Item",
         "description": "",
         "quantity": 10,
         "price": 100.00,
     }
     ```

3. **Update Item**
   - **Endpoint:** `/items/<int:item_id>/`
   - **Method:** `PUT`
   - **Request Body:**
   ```json
   {
       "name": "Updated Item",
       "quantity": 15,
       "price": 150.00
   }
   ```
   - **Response:**
     - Status: `200 OK`

4. **Delete Item**
   - **Endpoint:** `/items/<int:item_id>/`
   - **Method:** `DELETE`
   - **Response:**
     - Status: `204 No Content`

## Requirements

Ensure you have the following libraries in your `requirements.txt`:
```
Django>=4.2,<5.1
djangorestframework
djangorestframework-simplejwt
django-redis
```

## Environment Variables

Make sure your `.env` file contains:
- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_HOST`
- `DATABASE_PORT`
- `SECRET_KEY`

## Running the Project

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the API** at `http://127.0.0.1:8000/api/`.

## Testing

To run the test suite, use the following command:
```bash
python manage.py test inventory
```

This will execute the tests and report the results.
```

### Final Steps

- Replace placeholders (like `yourusername`, `db_name`, etc.) with your actual values.