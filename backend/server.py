from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

# Import models
from models.profile import Profile, ProfileUpdate, ContactInfo
from models.skills import Skills, SkillsUpdate, SkillCategory
from models.projects import Project, ProjectCreate, ProjectUpdate
from models.certificates import Certificate, CertificateCreate, CertificateUpdate
from models.education import Education, EducationCreate, EducationUpdate

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Portfolio API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Portfolio API is running", "status": "healthy"}

# Profile endpoints
@api_router.get("/profile", response_model=Profile)
async def get_profile():
    profile = await db.profile.find_one()
    if not profile:
        # Return seeded profile data if none exists
        return await seed_profile_data()
    
    # Convert MongoDB _id to id
    profile["id"] = str(profile.pop("_id"))
    return Profile(**profile)

@api_router.put("/profile", response_model=Profile)
async def update_profile(profile_update: ProfileUpdate):
    profile = await db.profile.find_one()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db.profile.update_one(
        {"_id": profile["_id"]},
        {"$set": update_data}
    )
    
    updated_profile = await db.profile.find_one({"_id": profile["_id"]})
    updated_profile["id"] = str(updated_profile.pop("_id"))
    return Profile(**updated_profile)

# Skills endpoints
@api_router.get("/skills", response_model=Skills)
async def get_skills():
    skills = await db.skills.find_one()
    if not skills:
        return await seed_skills_data()
    
    skills["id"] = str(skills.pop("_id"))
    return Skills(**skills)

@api_router.put("/skills", response_model=Skills)
async def update_skills(skills_update: SkillsUpdate):
    skills = await db.skills.find_one()
    if not skills:
        raise HTTPException(status_code=404, detail="Skills not found")
    
    update_data = skills_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db.skills.update_one(
        {"_id": skills["_id"]},
        {"$set": update_data}
    )
    
    updated_skills = await db.skills.find_one({"_id": skills["_id"]})
    updated_skills["id"] = str(updated_skills.pop("_id"))
    return Skills(**updated_skills)

# Projects endpoints
@api_router.get("/projects", response_model=List[Project])
async def get_projects(featured: Optional[bool] = None):
    query = {}
    if featured is not None:
        query["featured"] = featured
    
    projects_cursor = db.projects.find(query).sort("order", 1)
    projects = await projects_cursor.to_list(100)
    
    if not projects:
        return await seed_projects_data()
    
    # Convert MongoDB _id to id
    for project in projects:
        project["id"] = str(project.pop("_id"))
    
    return [Project(**project) for project in projects]

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    try:
        project = await db.projects.find_one({"id": project_id})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project["id"] = str(project.pop("_id"))
        return Project(**project)
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    project_dict = project.dict()
    project_dict["created_at"] = datetime.utcnow()
    project_dict["updated_at"] = datetime.utcnow()
    
    result = await db.projects.insert_one(project_dict)
    created_project = await db.projects.find_one({"_id": result.inserted_id})
    created_project["id"] = str(created_project.pop("_id"))
    
    return Project(**created_project)

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, project_update: ProjectUpdate):
    update_data = project_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.projects.update_one(
        {"id": project_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    updated_project = await db.projects.find_one({"id": project_id})
    updated_project["id"] = str(updated_project.pop("_id"))
    return Project(**updated_project)

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    result = await db.projects.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

# Certificates endpoints
@api_router.get("/certificates", response_model=List[Certificate])
async def get_certificates():
    certificates_cursor = db.certificates.find().sort("order", 1)
    certificates = await certificates_cursor.to_list(100)
    
    if not certificates:
        return await seed_certificates_data()
    
    for certificate in certificates:
        certificate["id"] = str(certificate.pop("_id"))
    
    return [Certificate(**certificate) for certificate in certificates]

@api_router.post("/certificates", response_model=Certificate)
async def create_certificate(certificate: CertificateCreate):
    certificate_dict = certificate.dict()
    certificate_dict["created_at"] = datetime.utcnow()
    
    result = await db.certificates.insert_one(certificate_dict)
    created_certificate = await db.certificates.find_one({"_id": result.inserted_id})
    created_certificate["id"] = str(created_certificate.pop("_id"))
    
    return Certificate(**created_certificate)

@api_router.put("/certificates/{certificate_id}", response_model=Certificate)
async def update_certificate(certificate_id: str, certificate_update: CertificateUpdate):
    update_data = certificate_update.dict(exclude_unset=True)
    
    result = await db.certificates.update_one(
        {"id": certificate_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    updated_certificate = await db.certificates.find_one({"id": certificate_id})
    updated_certificate["id"] = str(updated_certificate.pop("_id"))
    return Certificate(**updated_certificate)

@api_router.delete("/certificates/{certificate_id}")
async def delete_certificate(certificate_id: str):
    result = await db.certificates.delete_one({"id": certificate_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {"message": "Certificate deleted successfully"}

# Education endpoints
@api_router.get("/education", response_model=List[Education])
async def get_education():
    education_cursor = db.education.find().sort("order", 1)
    education_records = await education_cursor.to_list(100)
    
    if not education_records:
        return await seed_education_data()
    
    for education in education_records:
        education["id"] = str(education.pop("_id"))
    
    return [Education(**education) for education in education_records]

@api_router.post("/education", response_model=Education)
async def create_education(education: EducationCreate):
    education_dict = education.dict()
    education_dict["created_at"] = datetime.utcnow()
    
    result = await db.education.insert_one(education_dict)
    created_education = await db.education.find_one({"_id": result.inserted_id})
    created_education["id"] = str(created_education.pop("_id"))
    
    return Education(**created_education)

@api_router.put("/education/{education_id}", response_model=Education)
async def update_education(education_id: str, education_update: EducationUpdate):
    update_data = education_update.dict(exclude_unset=True)
    
    result = await db.education.update_one(
        {"id": education_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Education record not found")
    
    updated_education = await db.education.find_one({"id": education_id})
    updated_education["id"] = str(updated_education.pop("_id"))
    return Education(**updated_education)

@api_router.delete("/education/{education_id}")
async def delete_education(education_id: str):
    result = await db.education.delete_one({"id": education_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Education record not found")
    return {"message": "Education record deleted successfully"}

# Seed data functions
async def seed_profile_data():
    profile_data = {
        "name": "Building Systems That See: Karthik Pandala",
        "tagline": "Software engineer specializing in computer vision, AI, and seamless human-computer interaction",
        "bio": "I'm Karthik Pandala, a software engineer building systems that see. My focus is computer vision, AI, and real-time interaction—using technologies like OpenCV, TensorFlow, and PyTorch to create intuitive, responsive applications. I deliver clean code, robust solutions, and impactful projects—always user-focused and performance-tested.",
        "profile_image_url": "/api/placeholder/400/400",
        "contact": {
            "email": "karthikpandala0502@gmail.com",
            "phone": "+91 8688262873",
            "github": "https://github.com/karthikpandala",
            "linkedin": "https://linkedin.com/in/karthikpandala"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.profile.insert_one(profile_data)
    profile_data["id"] = str(result.inserted_id)
    profile_data.pop("_id", None)
    return Profile(**profile_data)

async def seed_skills_data():
    skills_data = {
        "categories": [
            {
                "name": "Computer Vision & AI",
                "items": ["OpenCV", "TensorFlow", "PyTorch", "Machine Learning", "Real-time Processing"],
                "order": 0
            },
            {
                "name": "Programming Languages",
                "items": ["Python", "JavaScript", "C/C++", "Java"],
                "order": 1
            },
            {
                "name": "Frameworks & Libraries",
                "items": ["Electron.js", "Node.js", "Streamlit", "REST APIs", "Spring Boot"],
                "order": 2
            },
            {
                "name": "Databases & Tools",
                "items": ["MySQL", "MongoDB", "Git", "Version Control", "SDLC"],
                "order": 3
            },
            {
                "name": "Core Concepts",
                "items": ["Computer Vision", "Interactive Systems", "Full-Stack Development", "Data Analysis", "Networking"],
                "order": 4
            }
        ],
        "updated_at": datetime.utcnow()
    }
    
    result = await db.skills.insert_one(skills_data)
    skills_data["id"] = str(result.inserted_id)
    skills_data.pop("_id", None)
    return Skills(**skills_data)

async def seed_projects_data():
    projects_data = [
        {
            "title": "Time Quacker: Gesture-Controlled Productivity Assistant",
            "status": "Completed",
            "description": "Real-time computer vision app enabling hands-free control of productivity tools through advanced gesture and face recognition technology.",
            "image_url": "https://images.unsplash.com/photo-1628233345409-349459e6f79a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwxfHxwcm9kdWN0aXZpdHklMjBhcHB8ZW58MHx8fHwxNzU0MDMwOTU3fDA&ixlib=rb-4.1.0&q=85",
            "tech_stack": ["JavaScript", "Electron.js", "OpenCV", "Computer Vision", "Web APIs"],
            "features": [
                "Gesture and face recognition via OpenCV for hands-free control",
                "Cross-platform Electron.js desktop app with system tray integration",
                "Hydration reminders, Pomodoro timer, and real-time weather integration",
                "Modular architecture tested for reliability and accuracy across platforms",
                "Real-time speech API integration with responsive user interface"
            ],
            "outcome": "Tested across platforms, improved productivity workflows, demonstrated at tech showcases",
            "github_link": "https://github.com/karthikpandala/time-quacker",
            "live_demo": None,
            "order": 0,
            "featured": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Real-Time Weather & Environmental Insight Engine",
            "status": "Active",
            "description": "Modern web application delivering live atmospheric data and intelligent weather alerts via OpenWeatherMap API integration.",
            "image_url": "https://images.unsplash.com/photo-1530563885674-66db50a1af19?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHx3ZWF0aGVyJTIwYXBwfGVufDB8fHx8MTc1NDAzMDk3MXww&ixlib=rb-4.1.0&q=85",
            "tech_stack": ["JavaScript", "Node.js", "Handlebars", "REST API", "CSS", "Cloud Computing"],
            "features": [
                "Real-time weather data integration with OpenWeatherMap API",
                "Responsive frontend design using modern templating frameworks",
                "Automated API validation and comprehensive error handling",
                "Cloud computing integration for improved data accuracy and insights",
                "Comprehensive unit and integration testing for system reliability"
            ],
            "outcome": "Deployed with 99.9% uptime, serving real-time data to users worldwide",
            "github_link": "https://github.com/karthikpandala/weather-engine",
            "live_demo": "https://weather-engine-demo.netlify.app",
            "order": 1,
            "featured": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "Movie Recommendation Engine",
            "status": "Completed",
            "description": "AI-powered, personalized movie suggestion system using collaborative filtering and advanced cosine similarity algorithms.",
            "image_url": "https://images.unsplash.com/photo-1685440663653-fa3e81dd109c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwzfHxzdHJlYW1pbmclMjBhcHB8ZW58MHx8fHwxNzU0MDMwOTc4fDA&ixlib=rb-4.1.0&q=85",
            "tech_stack": ["Python", "Machine Learning", "Streamlit", "Data Science", "Collaborative Filtering"],
            "features": [
                "Advanced cosine similarity algorithms for precise movie matching",
                "Interactive web interface built with Streamlit for seamless user experience",
                "Collaborative filtering techniques for personalized recommendations",
                "Functional programming approaches for efficient model training and optimization",
                "Data preprocessing pipeline with analytical insights and performance metrics"
            ],
            "outcome": "Achieved 92% user satisfaction rate with personalized recommendations",
            "github_link": "https://github.com/karthikpandala/movie-recommendation",
            "live_demo": "https://movie-recommender-kp.streamlit.app",
            "order": 2,
            "featured": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Insert all projects
    for project_data in projects_data:
        await db.projects.insert_one(project_data)
    
    # Return the projects
    projects_cursor = db.projects.find().sort("order", 1)
    projects = await projects_cursor.to_list(100)
    
    for project in projects:
        project["id"] = str(project.pop("_id"))
    
    return [Project(**project) for project in projects]

async def seed_certificates_data():
    certificates_data = [
        {
            "title": "AI and Data Science Hackathon Winner",
            "issuer": "Brainovision",
            "year": "2023",
            "description": "Won first place developing Optimized Manufacturing Planning (OMP) solutions for Aerospace Industry using Python, NumPy, Pandas, and Matplotlib. Demonstrated excellence in data analysis and algorithmic problem-solving under pressure.",
            "order": 0,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Advanced AI-ML and Data Science Workshop",
            "issuer": "Tech Innovation Institute",
            "year": "2023",
            "description": "Intensive 5-day workshop covering computer vision, machine learning algorithms, and data analytics using Python libraries. Gained hands-on experience with real-time data processing and model optimization.",
            "order": 1,
            "created_at": datetime.utcnow()
        },
        {
            "title": "Advanced Software Development & Professional Skills",
            "issuer": "Campus to Technical Careers Program",
            "year": "2023",
            "description": "Comprehensive training in full-stack development, covering Core Java 8, Hibernate, Spring Boot, and modern web technologies. Strengthened collaborative development and technical communication skills.",
            "order": 2,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Insert all certificates
    for cert_data in certificates_data:
        await db.certificates.insert_one(cert_data)
    
    # Return the certificates
    certificates_cursor = db.certificates.find().sort("order", 1)
    certificates = await certificates_cursor.to_list(100)
    
    for certificate in certificates:
        certificate["id"] = str(certificate.pop("_id"))
    
    return [Certificate(**certificate) for certificate in certificates]

async def seed_education_data():
    education_data = [
        {
            "degree": "Bachelor of Technology, Computer Science Engineering",
            "institution": "Sri Indu College of Engineering and Technology",
            "period": "2021 – 2025",
            "grade": "CGPA: 7.20",
            "location": "Hyderabad, Telangana",
            "order": 0,
            "created_at": datetime.utcnow()
        },
        {
            "degree": "Board of Intermediate Education",
            "institution": "Narayana Junior College",
            "period": "2019 – 2021",
            "grade": "Percentage: 74.2%",
            "location": "Hyderabad, Telangana",
            "order": 1,
            "created_at": datetime.utcnow()
        },
        {
            "degree": "Board of Secondary Education",
            "institution": "Naagarjuna High School",
            "period": "2019",
            "grade": "CGPA: 8.2",
            "location": "Hyderabad, Telangana",
            "order": 2,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Insert all education records
    for edu_data in education_data:
        await db.education.insert_one(edu_data)
    
    # Return the education records
    education_cursor = db.education.find().sort("order", 1)
    education_records = await education_cursor.to_list(100)
    
    for education in education_records:
        education["id"] = str(education.pop("_id"))
    
    return [Education(**education) for education in education_records]

# Include the router in the main app
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
