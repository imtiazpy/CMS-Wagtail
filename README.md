# 📚 CMS-Wagtail: A Modular Content Management System  

Welcome to the **CMS-Wagtail** project! This repository houses a fully functional and customizable CMS built with **Django** and **Wagtail**.

---

## Features
- 🖋️ Wagtail-powered CMS for robust content management.
- 🛠️ Dockerized for hassle-free deployment.
- 🐍 Python-based backend for clean, efficient development.
- 🌐 Flexible page creation mechanism. (not a fixed template for pages)
- 🌐 Multilingual (EN/DE)

---

## 🛠️ Setup Instructions

### Option 1: Running the Project with Docker
**Follow these steps for a smooth Docker setup:**

1. **Clone the Repository:**
   - Using SSH:
     ```bash
     git clone git@github.com:imtiazpy/CMS-Wagtail.git
     ```
   - Using HTTPS:
     ```bash
     git clone https://github.com/imtiazpy/CMS-Wagtail.git
     ```

2. **Navigate to the Project Directory:**
   ```bash
   cd CMS-Wagtail
   ```

3. **Create Environment Files:**
  - Create `.env` and `.env.db` files in the root directory.
  - Copy content from the sample files:
    ```bash
    cp .env.sample .env
    cp .env.db.sample .env.db
    ```

4. **Run the Project:**
  - Start Docker Compose:
    ```bash
    docker compose up -d --build
    ```
  - Wait for migrations and collectstatic to complete. To monitor logs:
    ```bash
    docker compose logs -f
    ```

5. **Create a Superuser:**
  - ```bash
    docker compose exec web python manage.py createsuperuser
    ```
    Follow the on-screen instructions.

6. **Access the Application:**
  - Main Site: http://127.0.0.1:1337/
  - Admin Panel: http://127.0.0.1:1337/admin/




## Option 2: Running the Project Without Docker  

Follow these steps for a local setup using Pipenv:

1. **Clone the Repository:**
   - Using SSH:
     ```bash
     git clone git@github.com:imtiazpy/CMS-Wagtail.git
     ```
   - Using HTTPS:
     ```bash
     git clone https://github.com/imtiazpy/CMS-Wagtail.git
     ```

2. **Navigate to the App Directory:**
   ```bash
   cd CMS-Wagtail/app/
   ```

3. **Create an Environment File:**
  - Create a .env file in the app directory.
  - Copy content from .env.sample:
  ```bash
  Copy content from .env.sample:
  ```

4. **Install Pipenv:**
  - If Pipenv is not installed, [follow the instructions here](https://pipenv.pypa.io/en/latest/) to install it.

5. **Activate the Virtual Environment:**
  ```bash
  pipenv shell
  ```

6. **Install Dependencies:**
  ```bash
  pipenv install
  ```

7. **Run Migrations:**
  ```
  python manage.py migrate
  ```

8. **Create a Superuser:**
  ```bash
  python manage.py createsuperuser
  ```

9. **Start the Server:**
  ```bash
  python manage.py runserver
  ```

Note: 
When using Pipenv, if you make any changes to the `.env` file, you need to exit the virtual environment and activate it again:
  - To exit: run `exit` from the terminal
  - To activate: run `pipenv shell` from the terminal


🤝 Let's Connect
If you have any questions, feedback, or just want to discuss this project, feel free to reach out!

📧 [Email Me](mailto:imtiazahmed.py@gmail.com)
💼 Catch Up with Me on [LinkedIn](https://www.linkedin.com/in/imtiazpy)
🐦 Follow Me on [Twitter](https://x.com/imtiazpy)
Thank you for checking out my project! Your feedback and thoughts are highly appreciated. Happy coding! 