# User and Note Management CLI
Welcome to my User and Note Management CLI project! This CLI application allows users to manage users and notes through a command-line interface. It leverages SQLAlchemy for object-relational mapping (ORM) and SQLite as the database backend.


## Table of Contents

- [Demo](#demo)
- [Technology](#Technology)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database](#database)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Demo

[ video]https://drive.google.com/file/d/1rmAddDjSMP6vmbVgTYCfTN0YzI-PfwAL/view
## Technology Stack
Python: The core language used for developing the CLI application.
SQLAlchemy: Utilized for object-relational mapping, simplifying database interactions.
SQLite: Chosen as the database backend for its lightweight nature and simplicity in setting up.

## Features

- **User Management**:
  - Create new users with a username, email, and optional role.
  - List all existing users.
  - Delete users by their user ID.
  - Update user information such as username, email, and role.

- **Note Management**:
  - Create new notes with a title, content, and associated user ID.
  - List all existing notes.
  - Delete notes by their note ID.
  - Update note information such as title and content.

- **Additional Functionality**:
  - Search for notes by keyword in their titles or content.
  - List notes created by a specific user.
  - List notes created on a particular date.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/your_repository.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your_repository
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the CLI application:

    ```bash
    python3 user_and_note.py
    ```

2. Use the available commands to manage users and notes. See the [Usage](#usage) section in the [README.md](README.md) file for more details.

## Database

By default, the application uses an SQLite database named `mydb.db`. You can change the database configuration in the `create_engine` function calls within the code.

## License

This project is licensed under the MIT License. See the [LICENSE] https://opensource.org/license/mit file for details.



## Acknowledgments

Special thanks to Ian mentor,the contributors and maintainers of SQLAlchemy for providing a powerful ORM tool.

## About the Developer

Hey there! 👋 I'm Josephine, a passionate student of software development at Moringa School. I have a keen interest in crafting elegant solutions to real-world problems using technology. Currently, I'm honing my skills in Python, SQL, and web development, among others always eager to learn and grow with each new challenge I encounter.
