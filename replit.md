# Vehicle Parking App V2

## Overview
A multi-user vehicle parking management application built with a Flask API backend and a Vue.js 3 SPA frontend (Vite). The app facilitates the management of parking lots, parking spots, and parked 4-wheeler vehicles. Its purpose is to provide a comprehensive solution for parking administration and user-side parking management, including booking, releasing, and viewing parking activities.

## User Preferences
- **Communication Style**: Clear, concise, and direct.
- **Coding Style**: Prioritize maintainability, readability, and adherence to best practices for Flask and Vue.js.
- **Workflow**: Iterative development is preferred. Focus on delivering functional components that can be built upon.
- **Interaction**: Ask for confirmation before implementing significant changes or making architectural decisions.
- **Working Preferences**:
    - Do not modify the core authentication logic without explicit instruction.
    - Ensure all changes are thoroughly tested and do not introduce regressions.
    - Prioritize security and performance in all implementations.

## System Architecture
The application uses a microservices-inspired architecture with a distinct backend API and a single-page application frontend.

### Backend (Flask API)
- **Framework**: Flask
- **Database**: SQLite (`backend/parking.db`) for primary data storage.
- **Authentication**: JWT-based token authentication with role-based access control (Admin/User). Token revocation is managed via a Redis blocklist.
- **Background Jobs**: Celery with Redis broker for asynchronous tasks (e.g., daily email reminders, monthly reports, CSV exports).
- **Caching**: Redis for API response caching to improve performance.
- **Email Service**: Gmail SMTP for sending email notifications.
- **API Design**: RESTful endpoints for managing users, parking lots, bookings, and providing dashboard statistics.

### Frontend (Vue.js 3 SPA)
- **Framework**: Vue.js 3 with Vite 5 for fast development and optimized builds.
- **Routing**: Vue Router 4 with navigation guards for role-based access.
- **State Management**: Vuex 4 for centralized application state, particularly for authentication.
- **HTTP Client**: Native Fetch API for all API interactions, including automatic JWT token handling.
- **UI/UX**: Modern, responsive design with a gradient theme, animated elements, and consistent styling across components using Bootstrap 5. Features a stylish landing page, detailed dashboards, and intuitive forms.
- **Charting**: Chart.js for data visualization in dashboards.

### Core Features
- **Authentication**: JWT-based, Admin/User roles, token revocation.
- **Admin Dashboard**: CRUD operations for parking lots, user management, summary statistics, and charts.
- **User Dashboard**: Parking spot booking/release, booking history, personal statistics, and CSV export.
- **Email Notifications**: Daily reminders and monthly activity reports via Gmail SMTP.
- **Performance**: Redis caching for API, optimized frontend build.

## External Dependencies
- **Database**: SQLite (`backend/parking.db`)
- **Caching & Job Queue**: Redis
- **Email Service**: Gmail SMTP (via `parkhere870@gmail.com`)
- **PDF Generation**: ReportLab
- **Charting**: Chart.js
- **Icons**: Bootstrap Icons