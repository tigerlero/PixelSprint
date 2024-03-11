# PixelSprint

PixelSprint is a Django project for managing tasks and projects.

## Features

It will include:
- [x] Create Task
- [x] Delete Task
- [x] Update Basic Info of Task
- [x] Display Priority of Task, Assigned User Image or Gravatar, Desciprion,
- [x] Update Status and Position in Kanban Task
- [x] Update Assigned User in Kanban Task
- [x] Create Prohect
- [x] Update Project
- [x] Delete Project
- [x] Get Tasks of Project
- [x] Profil Image Uploading
- [x] Profil Avator Color Choose
- [x] XP gained if task is in last column of Kanban
- [ ] Level Up based on XP
- [x] Create Note
- [x] Update Note
- [x] Delete Note
- [x] Subtasks
- [ ] Kanban for Project


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
