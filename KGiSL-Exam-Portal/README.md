# Sinthanai's Exam Portal

KGiSL Institute of Technology - Exam Management System

## Features

- **Admin Dashboard**: Upload seating plans, manage datasets, toggle active exams
- **Student Portal**: View hall seating details, exam information
- **Excel Upload**: Supports both .xls and .xlsx formats, including corrupted database exports
- **Faculty Management**: Sync faculty data from Google Sheets (supports multi-sheet workbooks), automated allocation
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

## Maintainers

- **Faculty-In-Charge**: Admin Team
- **Technical Lead**: Dev Team

## Project Structure

```
30: exam-portal/
31: ├── backend/              # Django backend service
32: │   ├── manage.py         # Entry point for administrative tasks
33: │   ├── backend/          # Project-level configuration and settings
34: │   ├── apps/             # Application modules (core, exams, faculty)
35: │   ├── datasets/         # Storage for uploaded Excel seating plans
36: │   ├── scripts/          # Utility and maintenance scripts
37: │   └── requirements.txt  # Python dependency list
38: └── frontend/             # Next.js frontend application
39:     ├── src/app/          # Page routes and components
40:     ├── public/           # Static assets (images, icons)
41:     └── package.json      # Node.js dependencies and scripts
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


## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/name`).
3. Commit your changes (`git commit -m "feat: add new feature"`).
4. Push to the branch (`git push origin feature/name`).
5. Open a Pull Request.

Please ensure all tests pass before submitting.

