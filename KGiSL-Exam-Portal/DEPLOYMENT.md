# Deployment Guide - Exam Portal Management System on Render

## Prerequisites
- GitHub account with repository: `https://github.com/Vignesh5432/Exam_Portal_Management.git`
- Render account (sign up at https://render.com)

## Deployment Steps

### Step 1: Push Configuration Files to GitHub

All configuration files have been created. Push them to your repository:

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `exam-portal-db`
   - **Database**: `exam_portal_db`
   - **User**: `exam_portal_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free
4. Click **"Create Database"**
5. **Save the Internal Database URL** (you'll need this for the backend)

### Step 3: Deploy Django Backend

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Vignesh5432/Exam_Portal_Management`
3. Configure:
   - **Name**: `exam-portal-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root of repo)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn backend.wsgi:application`
   - **Plan**: Free

4. **Add Environment Variables** (click "Advanced" → "Add Environment Variable"):

   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | Generate a secure random string (use https://djecrety.ir/) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `exam-portal-backend.onrender.com` (use your actual backend URL) |
   | `DATABASE_URL` | Paste the Internal Database URL from Step 2 |
   | `CORS_ALLOWED_ORIGINS` | `https://exam-portal-frontend.onrender.com` (use your actual frontend URL) |
   | `PYTHON_VERSION` | `3.11.0` |

5. Click **"Create Web Service"**
6. Wait for deployment to complete (5-10 minutes)
7. **Copy your backend URL** (e.g., `https://exam-portal-backend.onrender.com`)

### Step 4: Deploy Next.js Frontend

1. Click **"New +"** → **"Web Service"**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `exam-portal-frontend`
   - **Region**: Same as backend
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Runtime**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Free

4. **Add Environment Variables**:

   | Key | Value |
   |-----|-------|
   | `NEXT_PUBLIC_API_URL` | Your backend URL from Step 3 |
   | `NODE_VERSION` | `20.11.0` |

5. Click **"Create Web Service"**
6. Wait for deployment to complete

### Step 5: Update CORS Settings

After both services are deployed:

1. Go to your backend service on Render
2. Update the `CORS_ALLOWED_ORIGINS` environment variable with your actual frontend URL
3. Update `ALLOWED_HOSTS` to include your backend domain
4. The service will automatically redeploy

### Step 6: Create Admin User

1. Go to your backend service on Render
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin account

### Step 7: Load Initial Data (Optional)

If you need to load hall ticket data or other datasets:

1. In the backend Shell on Render:
   ```bash
   python load_hall_ticket_data.py
   ```

## Environment Variables Reference

### Backend Environment Variables

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=exam-portal-backend.onrender.com,your-custom-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
CORS_ALLOWED_ORIGINS=https://exam-portal-frontend.onrender.com
PYTHON_VERSION=3.11.0
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=https://exam-portal-backend.onrender.com
NODE_VERSION=20.11.0
```

## Post-Deployment Verification

### Test Backend
1. Visit `https://your-backend-url.onrender.com/admin`
2. Login with superuser credentials
3. Verify admin panel loads correctly

### Test Frontend
1. Visit `https://your-frontend-url.onrender.com`
2. Test login functionality
3. Verify student portal features
4. Test hall ticket generation

### Test API Endpoints
```bash
# Health check
curl https://your-backend-url.onrender.com/api/

# Test authentication
curl -X POST https://your-backend-url.onrender.com/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `build.sh` has correct permissions

### Database Connection Error
- Verify `DATABASE_URL` is correctly set
- Check database is in same region as backend
- Ensure database is running

### Static Files Not Loading
- Verify `STATIC_ROOT` is set in settings.py
- Check whitenoise is in `MIDDLEWARE`
- Run `python manage.py collectstatic` in Shell

### CORS Errors
- Update `CORS_ALLOWED_ORIGINS` with correct frontend URL
- Ensure no trailing slashes in URLs
- Check browser console for exact error

### Frontend Can't Connect to Backend
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is deployed and running
- Test backend URL directly in browser

## Free Tier Limitations

⚠️ **Important**: Render free tier services:
- Spin down after 15 minutes of inactivity
- Take 30-60 seconds to spin up on first request
- Have 750 hours/month limit per service
- PostgreSQL database has 90-day expiration (backup your data!)

## Custom Domain (Optional)

To use a custom domain:
1. Go to service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed
5. Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`

## Monitoring

- View logs in Render dashboard under "Logs" tab
- Set up email notifications for deployment failures
- Monitor database usage in database dashboard

## Support

For issues:
- Check Render documentation: https://render.com/docs
- Review Django deployment guide: https://docs.djangoproject.com/en/stable/howto/deployment/
- Check Next.js deployment docs: https://nextjs.org/docs/deployment

---

**Your Application URLs:**
- Backend: `https://exam-portal-backend.onrender.com`
- Frontend: `https://exam-portal-frontend.onrender.com`
- Admin Panel: `https://exam-portal-backend.onrender.com/admin`

🎉 **Deployment Complete!**
