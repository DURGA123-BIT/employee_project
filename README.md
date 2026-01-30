# Employee Management System (EMS)

A role-based web application for managing tasks, projects, users,
notifications, and reports.

## Tech Stack

-   Backend: Django (Python)
-   Templates: HTML, Bootstrap5
-   Database: SQLite / MySQL
-   Reports: CSV, Excel, PDF
-   Charts: Chart.js
-   Auth: Django Authentication
-   Notifications: Internal Alerts

## User Roles

-   Admin (full access)
-   Manager (project & task management)
-   Employee (assigned tasks only)

## Features

-   Authentication + Role dashboards
-   User management
-   Projects module
-   Tasks module with priority, status, due-date & progress
-   Employee task updates + comments + file uploads
-   Manager approval workflow
-   Notifications + badge count
-   Activity logs
-   Reports with filters + charts
-   Export: CSV, Excel, PDF

## Status Workflow

-   PENDING → ONGOING → COMPLETED → APPROVED

## Reports

Includes: - Total tasks - Completed - Pending - Ongoing - Total
projects - Total employees - Pie chart view - Export options

## Installation

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

## Login Redirect

-   Admin -\> /admin-dashboard
-   Manager -\> /manager-dashboard
-   Employee -\> /employee-dashboard

## Completion Status

✔ Core features completed\
✔ UI completed\
✔ Reporting & exports completed\
✔ Notifications & logs completed


