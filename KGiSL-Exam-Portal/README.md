# Sinthanai's Exam Portal

KGiSL Institute of Technology - Exam Management System

## Features

- **Admin Dashboard**: Upload seating plans, manage datasets, toggle active exams
- **Student Portal**: View hall seating details, exam information
- **Excel Upload**: Supports both .xls and .xlsx formats, including corrupted database exports
- **Mobile Responsive**: Works seamlessly on all devices

## Tech Stack

### Backend
- Django 5.2.9
- Django REST Framework
- Python 3.x
- PostgreSQL (Production) / MySQL (Local Development)

### Frontend
- Next.js 16.0.10
- React
- Tailwind CSS
- Framer Motion
- Axios

## Project Structure

```
exam-portal/
├── backend/              # Django backend
│   ├── manage.py
│   ├── backend/         # Django project settings
│   ├── apps/            # Django apps (core, exams)
│   ├── datasets/        # Uploaded Excel files
│   ├── scripts/         # Utility scripts
│   └── requirements.txt
└── frontend/            # Next.js frontend
    ├── src/app/
    ├── public/
    └── package.json
```

## Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python scripts/create_admin.py  # Create admin user
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

### Admin Login
1. Navigate to http://localhost:3000
2. Select "Admin" role
3. Login with admin credentials
4. Upload seating plan (.xls or .xlsx)
5. Toggle dataset to activate

### Student Login
1. Navigate to http://localhost:3000
2. Select "Student" role
3. Enter register number and password
4. View hall seating details

## Deployment

### Render Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Render deployment instructions.

- Backend: Deploy Django app to Render with PostgreSQL
- Frontend: Deploy Next.js app to Render or Vercel
- Update `NEXT_PUBLIC_API_URL` in frontend environment variables

## License

© 2025 KGiSL Institute of Technology

