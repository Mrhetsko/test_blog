# FastAPI Task - Simple Blog API

This is a simple web application built with FastAPI as part of a technical assessment. The application provides basic user authentication (signup, login) and CRUD functionality for text posts.

It follows a layered architecture, separating concerns into routing, business logic (CRUD), and database models.

---

## Tech Stack

*   **Backend:** Python 3.12, FastAPI
*   **Database:** MySQL 8.0
*   **ORM:** SQLAlchemy
*   **Database Driver:** PyMySQL
*   **Deployment:** Docker for the database

---

## How to Set Up and Run the Project

### Prerequisites

*   Python 3.10+ and `pip`
*   Docker and Docker Compose
*   Git

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create the virtual environment

```sh
python3 -m venv venv
```

### 3. Activate it
```
source venv/bin/activate
```

### 4. Run the Database using Docker
The application is configured to connect to a MySQL database. The fastest way to get one running is with Docker.
Run the following command in your terminal. This will download the official MySQL 8 image, start a container, and automatically create the required database.

```sh
docker run -d --name mysql-db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysecretpassword -e MYSQL_DATABASE=fastapi_task_db mysql:8.0
```

### 5. Run the Application
```sh
uvicorn main:app --reload
```
# test_blog
# test_blog
# test_blog
