# Resume Screening Backend

FastAPI backend for resume screening and candidate ranking using ML embeddings and clustering.

## Features

- PDF resume text extraction
- Text preprocessing and embedding generation
- Similarity scoring against job descriptions
- Skill extraction
- Candidate clustering
- CSV export functionality

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Deployment on Railway.app (Docker)

### Prerequisites

- Docker installed locally (for testing)
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))

### Local Docker Testing

1. **Build the Docker image**:
```bash
docker build -t resume-screening-api .
```

2. **Run the container**:
```bash
docker run -p 8000:8000 resume-screening-api
```

3. **Test the API**:
   - Open `http://localhost:8000` in your browser

### Deploy to Railway

1. **Sign up/Login** to [Railway.app](https://railway.app)

2. **Create a New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account if not already connected
   - Select your repository: `resume_screening_backend`

3. **Railway will automatically detect Docker**:
   - Railway will find the `Dockerfile` and use it automatically
   - No additional configuration needed!

4. **Configure Environment** (Optional):
   - Railway automatically sets `PORT` environment variable
   - The app will use port 8000 by default (Railway maps it automatically)

5. **Deploy**:
   - Railway will automatically build and deploy your Docker container
   - You'll get a URL like `https://your-app.railway.app`

### Railway Features

- **Free Tier**: $5 credit/month (usually enough for small apps)
- **Persistent Storage**: Railway provides persistent volumes for file storage
- **No Sleep**: Services stay awake (unlike Render free tier)
- **Auto Deploy**: Automatically deploys on git push
- **Logs**: Real-time logs in Railway dashboard

### Adding Persistent Volume (for uploads)

1. In Railway dashboard, go to your service
2. Click "Variables" tab
3. Add a volume:
   - Click "Add Volume"
   - Mount path: `/app/uploads`
   - Size: 1GB (or as needed)

Note: You may need to update `main.py` to use the volume path if you add one.

## Environment Variables

No environment variables required for basic operation. The app uses:
- `PORT` (automatically set by Railway)

## API Endpoints

- `GET /` - Health check
- `POST /upload_resume` - Upload and extract text from PDF resume
- `POST /process_resume` - Process resume against job description
- `GET /top_candidates` - Get ranked candidates
- `GET /clusters` - Get cluster visualization data
- `GET /export_csv` - Export candidates as CSV
- `DELETE /resume/{resume_id}` - Delete a resume
- `DELETE /resumes` - Delete all resumes

## Notes

- Railway automatically detects and builds from Dockerfile
- The Docker image includes all dependencies and is ready to deploy
- Railway provides persistent storage volumes if needed for file uploads
- Services stay awake on Railway (no sleep/wake delays like Render free tier)

