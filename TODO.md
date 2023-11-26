# Manifest for Program SKE-FP

- Author: taamtera
- Co-Author: Paruj Ratanaworabhan
- License: KU
- Version: V4.12

- Program Overview:
    This program, named "SKE_FP_V4.12," is a project management system designed to facilitate the coordination and management of academic projects within a university setting. It provides functionalities for users with different roles such as administrators, faculty members, and students to interact with and manage project-related data.
    

### Key Features

- **Admin Mode:**
  - Powerful tool for debugging
  
- **Easy Search:**
  - Search data using Names or ID case Insensitive.

- **User Interface:**
  - Simple console-based interface for ease of use.
  
- **Multiple Roles:**
  - One person can assume many roles in many different projects.
  
- **Multiple Users:**
  - Supports real-time interactions for multiple users loged in at the same time.

- **Real DB**
  - Realistic and scalable Database system for searching and filtering data

## System Functionality

- Random IDs are generated for new projects.
- The system clears the screen for a cleaner interface.
- Modified data is saved to CSV files after each operation.
- database with ignore case searching functions

### User Interactions

- **Faculty:**
  - login with faculty ID and password.
  - View and manage projects advised by them.
  - View all projects
  - Accept or decline project invitations from students.
  - Main menu for viewing requests and managing projects.
  - Option to accept or decline project requests.
  - Option to accept or decline publish requests.
  - Exit the system.

- **Student:**
  - login with student ID and password.
  - View and manage projects they are involved in.
  - Ability to create and delete projects.
  - Ability invite and remove project
  - Ability to accept or decline project invitations.
  - Ability to submit projects for review.
  - Ability to submit report for review.
  - Request faculty advisor for a project.
  - Accept or decline invitations to join projects.
  - Submit completed projects.

- **Admin:**
  - login with admin credentials.
  - View all projects
  - **Admin Mode:**
    - Edit user information of the dataa base.
    - Perform database maintenance.
    - Exit admin mode.

### Notes
- Actions are role-specific, providing a tailored experience for each user type.
- System handles project requests, creation, and user management.
- Program uses a console-based interface for simplicity and ease of use
- Security could be improved