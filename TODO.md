# Project Management System Overview

### Key Features

- **Admin Mode:**
  - Powerful tool for debugging
  
- **Easy Search:**
  - Search data using Names or ID

- **User Interface:**
  - Simple console-based interface for ease of use.
  
- **Multiple Roles:**
  - One person can assume many roles in different projects.
  
- **Multiple Users:**
  - Supports real-time interactions for multiple users.

- **Real DB**
  - Realistic and scalable Database system for searching and filtering data

## User Roles

### Faculty
- **Actions:**
  - View and manage own projects.
  - Accept or decline project requests from students.
  - Submit projects to the system.

### Student
- **Actions:**
  - View and manage own projects.
  - Request faculty advisor for a project.
  - Accept or decline project invitations.
  - Create new projects.

### Admin
- **Actions:**
  - Edit database tables (for system maintenance).
  - Access admin mode to edit user information.

## User Interactions

### Faculty
- **Login:**
  - Enter username (e.g., faculty ID) and password.
- **Main Menu:**
  - View project requests.
  - Select and manage own projects.
  - Accept or decline project requests.
  - Submit projects for review.
  - Exit the system.

### Student
- **Login:**
  - Enter username (e.g., student ID) and password.
- **Main Menu:**
  - View project requests.
  - Select and manage own projects.
  - Request a faculty advisor.
  - Accept or decline project invitations.
  - Create new projects.
  - Exit the system.

### Admin
- **Login:**
  - Enter admin credentials.
- **Admin Mode:**
  - Edit user information (faculty and student details).
  - Perform database maintenance.
  - Exit admin mode.

## Project Interactions

- **Faculty:**
  - View and manage projects advised by them.
  - Accept or decline project invitations from students.
  - Submit completed projects.

- **Student:**
  - View and manage projects they are involved in.
  - Request faculty advisors for their projects.
  - Accept or decline invitations to join projects.
  - Create new projects.

## System Functionality

- Random IDs are generated for new projects.
- The system clears the screen for a cleaner interface.
- Modified data is saved to CSV files after each operation.

## Key Features

### User Roles and Actions

- **Faculty:**
  - View and manage own projects.
  - Accept or decline project requests from students.
  - Submit projects to the system.

- **Student:**
  - View and manage own projects.
  - Request faculty advisor for a project.
  - Accept or decline project invitations.
  - Create new projects.

- **Admin:**
  - Edit database tables for system maintenance.
  - Access admin mode to edit user information.

### User Interactions

- **Faculty:**
  - Secure login with faculty ID and password.
  - Main menu for viewing requests and managing projects.
  - Option to accept or decline project requests.
  - Ability to submit projects for review.
  - Exit the system.

- **Student:**
  - Secure login with student ID and password.
  - Main menu for viewing requests and managing projects.
  - Option to request a faculty advisor.
  - Ability to accept or decline project invitations.
  - Option to create new projects.
  - Exit the system.

- **Admin:**
  - Secure login with admin credentials.
  - Admin mode for editing user information and performing maintenance.
  - Ability to exit admin mode.

### Project Interactions

- **Faculty:**
  - View and manage projects advised by them.
  - Accept or decline project invitations from students.
  - Submit completed projects.

- **Student:**
  - View and manage projects they are involved in.
  - Request faculty advisors for their projects.
  - Accept or decline invitations to join projects.
  - Create new projects.

### Notes

- Actions are role-specific, providing a tailored experience for each user type.
- System handles project requests, creation, and user management.
- Program uses a console-based interface for simplicity and ease of use
- Security could be improved (user role permission issues)