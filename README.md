# Resume Screening Project

A full-stack application for screening resumes, ranking candidates based on job descriptions, and visualizing candidate clusters.

## Project Structure

```
resume_screening/
├── frontend/          # Flutter application
│   ├── lib/
│   │   ├── main.dart
│   │   ├── models/
│   │   ├── screens/
│   │   └── services/
│   └── pubspec.yaml
├── backend/           # FastAPI application
│   ├── main.py
│   ├── modules/
│   │   ├── pdf_extractor.py
│   │   ├── preprocessor.py
│   │   ├── embedder.py
│   │   ├── similarity.py
│   │   ├── skill_extractor.py
│   │   ├── clusterer.py
│   │   └── data_store.py
│   ├── requirements.txt
│   ├── uploads/       # Uploaded resumes stored here
│   └── example_resumes/  # Example PDFs for testing
└── README.md
```

## Features

### Backend (FastAPI)
- PDF text extraction
- Text preprocessing and cleaning
- Embedding generation using sentence-transformers
- Resume-job similarity scoring
- Skill extraction from resumes
- Candidate clustering using KMeans
- PCA-based visualization coordinates
- CSV export of ranked candidates

### Frontend (Flutter)
- Resume upload page (PDF)
- Job description input page
- Candidate ranking page with similarity scores
- Cluster visualization page (2D scatter plot)
- CSV download functionality

