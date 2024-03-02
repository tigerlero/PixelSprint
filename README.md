# PixelSprint

PixelSprint is a Django project for managing tasks and projects.

## Features

- **Task Management**: Organize and track tasks using a Kanban-style board.
- **User Profiles**: Customize your profile with a profile picture and other details.
- **Gravatar Integration**: Automatically fetch user profile pictures from Gravatar.
- **Priority Levels**: Assign priority levels to tasks (Critical, High, Medium, Low).
- **XP Rewards**: Earn XP for completing tasks.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/tigerlero/PixelSprint.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure Django settings:

    - Set up your database in the `settings.py` file.
    - Set the `SECRET_KEY` (consider using environment variables).

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

6. Open your browser and navigate to [http://localhost:8000](http://localhost:8000).

## Configuration

- **Secret Key**: Keep the `SECRET_KEY` secret. Use environment variables for security.
- **Allowed Hosts**: Specify allowed hosts in production settings.
- **Database**: Configure your database settings for production (e.g., PostgreSQL).
- **Static and Media Files**: Configure `STATIC_ROOT` and `MEDIA_ROOT` for production.
- **Debug Setting**: Set `DEBUG` to `False` in production for better security.
- **Logging Configuration**: Configure logging settings for production.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Your contributions are welcome!
