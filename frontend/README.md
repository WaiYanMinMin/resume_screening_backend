# Resume Screening Flutter Frontend

Flutter application for resume screening with candidate ranking and cluster visualization.

## Setup

1. Make sure Flutter is installed on your system
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   flutter pub get
   ```

4. Run the app:
   ```bash
   flutter run
   ```

## Pages

- **Upload Page**: Upload PDF resumes
- **Job Description Page**: Enter job description to match against resumes
- **Ranking Page**: View ranked candidates with similarity scores, skills, and cluster labels
- **Visualization Page**: View 2D scatter plot of candidate clusters

## Configuration

The API base URL is set in `lib/services/api_service.dart`. Default is `http://localhost:8000`. Update this if your backend runs on a different address.

## Features

- PDF file upload
- Real-time candidate ranking
- Skill extraction display
- Cluster visualization with PCA
- CSV export functionality

