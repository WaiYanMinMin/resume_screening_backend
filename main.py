from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Dict
from pydantic import BaseModel
import uvicorn
import os
import tempfile
import uuid as uuid_lib
from pathlib import Path

from modules.pdf_extractor import PDFExtractor
from modules.preprocessor import TextPreprocessor
from modules.embedder import Embedder
from modules.similarity import SimilarityCalculator
from modules.skill_extractor import SkillExtractor
from modules.clusterer import Clusterer
from modules.data_store import DataStore
import numpy as np
app = FastAPI(title="Resume Screening API")

# Enable CORS for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
pdf_extractor = PDFExtractor()
preprocessor = TextPreprocessor()
embedder = Embedder()
similarity_calc = SimilarityCalculator()
skill_extractor = SkillExtractor()
clusterer = Clusterer()
data_store = DataStore()

# Use temporary directory for PDF processing (files deleted after extraction)
TEMP_DIR = Path(tempfile.gettempdir()) / "resume_uploads"
TEMP_DIR.mkdir(exist_ok=True)

# Pydantic models
class ProcessResumeRequest(BaseModel):
    resume_id: str
    job_description: str

@app.get("/")
async def root():
    return {"message": "Resume Screening API"}

@app.delete("/resume/{resume_id}")
async def delete_resume(resume_id: str):
    """Delete a resume by ID"""
    try:
        deleted = data_store.delete_resume(resume_id)
        if deleted:
            return {"message": f"Resume {resume_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Resume not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/resumes")
async def delete_all_resumes():
    """Delete all resumes"""
    try:
        data_store.clear_all()
        return {"message": "All resumes deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload a PDF resume and extract text (file is deleted after extraction)"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Create temporary file for PDF processing
        # Use unique temp filename to avoid conflicts
        temp_filename = f"{uuid_lib.uuid4()}_{file.filename}"
        file_path = TEMP_DIR / temp_filename
        
        try:
            # Save uploaded file temporarily
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Extract text from PDF
            text = pdf_extractor.extract_text(str(file_path))
            
            # Store resume data (in-memory only, no file storage)
            resume_id = data_store.add_resume(file.filename, text)
            
            return {
                "resume_id": resume_id,
                "filename": file.filename,
                "text": text[:500] + "..." if len(text) > 500 else text  # Preview
            }
        finally:
            # Always delete the temporary file after processing
            if file_path.exists():
                file_path.unlink()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_resume")
async def process_resume(request: ProcessResumeRequest):
    """Process a resume against a job description"""
    try:
        resume_id = request.resume_id
        job_description = request.job_description
        resume = data_store.get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_text = resume["text"]
        job_desc = job_description
        
        # Preprocess texts
        processed_resume = preprocessor.preprocess(resume_text)
        processed_job = preprocessor.preprocess(job_desc)
        
        # Generate embeddings
        resume_embedding = embedder.embed(processed_resume)
        job_embedding = embedder.embed(processed_job)
        
        # Calculate similarity
        similarity_score = similarity_calc.cosine_similarity(resume_embedding, job_embedding)
        
        # Extract skills
        skills = skill_extractor.extract_skills(resume_text)
        
        # Add embedding to clusterer for clustering
        clusterer.add_embedding(resume_embedding)
        
        # Get cluster assignment (will be computed if not already done)
        cluster_label = clusterer.assign_cluster(resume_embedding)
        
        # Update resume data
        data_store.update_resume_processing(
            resume_id,
            similarity_score,
            skills,
            cluster_label,
            resume_embedding.tolist()
        )
        
        return {
            "resume_id": resume_id,
            "similarity_score": float(similarity_score),
            "skills": skills,
            "cluster_label": int(cluster_label)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/top_candidates")
async def top_candidates(job_description: str = ""):
    """Get ranked candidates sorted by similarity score"""
    try:
        candidates = data_store.get_all_candidates()
        
        if not candidates:
            return {"candidates": []}
        
        # If job description provided, process all candidates
        if job_description:
            processed_job = preprocessor.preprocess(job_description)
            job_embedding = embedder.embed(processed_job)
            
         
            
            for candidate in candidates:
                resume_emb = None
                
                # Generate embedding if it doesn't exist
                if not candidate.get("embedding"):
                    resume_text = candidate.get("text", "")
                    if resume_text:
                        processed_resume = preprocessor.preprocess(resume_text)
                        resume_emb = embedder.embed(processed_resume)
                        # Add embedding to clusterer
                        clusterer.add_embedding(resume_emb)
                        # Get cluster assignment
                        cluster_label = clusterer.assign_cluster(resume_emb)
                        # Extract skills
                        skills = skill_extractor.extract_skills(resume_text)
                        # Update candidate data
                        candidate["embedding"] = resume_emb.tolist()
                        candidate["cluster_label"] = int(cluster_label)
                        candidate["skills"] = skills
                    else:
                        # No text available, skip
                        continue
                else:
                    # Use existing embedding
                    resume_emb = candidate["embedding"]
                    # Convert list to numpy array if needed
                    if isinstance(resume_emb, list):
                        resume_emb = np.array(resume_emb)
                
                # Calculate similarity
                similarity = similarity_calc.cosine_similarity(
                    resume_emb, job_embedding
                )
                candidate["similarity_score"] = float(similarity)
        
        # Sort by similarity score (descending)
        ranked_candidates = sorted(
            candidates,
            key=lambda x: x.get("similarity_score", 0.0),
            reverse=True
        )
        
        return {"candidates": ranked_candidates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clusters")
async def get_clusters():
    """Get cluster visualization data (PCA/t-SNE coordinates)"""
    try:
        candidates = data_store.get_all_candidates()
        
        if len(candidates) < 2:
            return {
                "coordinates": [],
                "cluster_labels": [],
                "resume_ids": []
            }
        
        # Get embeddings and labels
        embeddings = []
        cluster_labels = []
        resume_ids = []
        
        for candidate in candidates:
            if candidate.get("embedding"):
                emb = candidate["embedding"]
                # Convert list to numpy array if needed
                if isinstance(emb, list):
                    emb = np.array(emb)
                embeddings.append(emb)
                cluster_labels.append(candidate.get("cluster_label", 0))
                resume_ids.append(candidate["resume_id"])
        
        if not embeddings:
            return {
                "coordinates": [],
                "cluster_labels": [],
                "resume_ids": []
            }
        
        # Get 2D coordinates for visualization
        coordinates = clusterer.get_visualization_coordinates(embeddings)
        
        return {
            "coordinates": coordinates.tolist(),
            "cluster_labels": cluster_labels,
            "resume_ids": resume_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export_csv")
async def export_csv():
    """Export ranked candidates as CSV"""
    try:
        candidates = data_store.get_all_candidates()
        
        # Sort by similarity score
        ranked_candidates = sorted(
            candidates,
            key=lambda x: x.get("similarity_score", 0.0),
            reverse=True
        )
        
        # Generate CSV
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "Rank", "Resume ID", "Filename", "Similarity Score",
            "Skills", "Cluster Label"
        ])
        
        # Data rows
        for rank, candidate in enumerate(ranked_candidates, 1):
            writer.writerow([
                rank,
                candidate["resume_id"],
                candidate["filename"],
                f"{candidate.get('similarity_score', 0.0):.4f}",
                ", ".join(candidate.get("skills", [])),
                candidate.get("cluster_label", 0)
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=ranked_candidates.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

