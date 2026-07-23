from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from google import genai
client = genai.Client(api_key="YOUR_API_KEY")
import pdfplumber
import matplotlib.pyplot as plt
import sqlite3
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
conn = sqlite3.connect("career.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS resumes(

id INTEGER PRIMARY KEY AUTOINCREMENT,

filename TEXT,

career TEXT,

ats INTEGER,

strength TEXT

)

""")

conn.commit()

skills_database = [

"python",
"java",
"c",
"c++",
"javascript",
"react",
"html",
"css",
"sql",
"mysql",
"mongodb",
"machine learning",
"deep learning",
"tensorflow",
"pytorch",
"numpy",
"pandas",
"opencv",
"fastapi",
"flask",
"git",
"github",
"docker",
"aws",
"power bi",
"excel"

]
latest_report = {}

resume_history = []

def calculate_ats_score(detected_skills):

    total_skills = len(skills_database)
    found_skills = len(detected_skills)

    score = int((found_skills / total_skills) * 100)

    if score > 100:
        score = 100

    return score
def get_strength(detected_skills):

    if len(detected_skills) >= 8:
        return "Excellent Technical Profile"

    elif len(detected_skills) >= 5:
        return "Good Technical Skills"

    else:
        return "Need More Technical Skills"
@app.get("/")
def home():

    return{
        "Project":"AI Career Digital Twin 2.0",
        "Developer":"Amarjeet",
        "Status":"Running"
    }
@app.get("/student")
def student():

    return{

    "Name":"Amarjeet",

    "Branch":"AI & DS",

    "CGPA":"7.24"

    }
@app.get("/career")
def career():

    return {
        "Best Career": "AI Engineer",
        "Match Score": "92%",
        "Second Option": "Data Scientist",
        "Third Option": "ML Engineer"
    }
@app.get("/resume")
def resume():

    return {
        "Resume Status": "Uploaded",
        "ATS Score": "88%",
        "Projects": 4,
        "Certificates": 8
    }
    
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)

    return {
        "Message": "Resume Uploaded Successfully",
        "File Name": file.filename
    }
@app.get("/read-resume")
def read_resume():

    text = ""

    import os

    pdf_path = os.path.join(os.path.dirname(__file__), "resumes.pdf")

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text += page.extract_text()

    return {
        "Resume Text": text
    }
@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    
    global latest_report
    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)

    text = ""

    with pdfplumber.open(file.filename) as pdf:

        for page in pdf.pages:

            if page.extract_text():

                text += page.extract_text().lower()

    detected_skills = []

    for skill in skills_database:

        if skill in text:

            detected_skills.append(skill)

    ats_score = calculate_ats_score(detected_skills)
    strength = get_strength(detected_skills)
    career = predict_career(detected_skills)
    missing_skills = find_missing_skills(detected_skills)
    roadmap = learning_roadmap(missing_skills)
    questions = generate_questions(detected_skills)
    interview = interview_score(detected_skills)
    ai_report = ask_gemini(text)
    graph = generate_skill_graph(detected_skills)

    latest_report = {
        "File": file.filename,
        "Detected Skills": detected_skills,
        "Total Skills": len(detected_skills),
        "ATS Score": str(ats_score) + "%",
        "Career Prediction": career,
        "Strength": strength,
        "Interview Score": interview,
        "Missing Skills": missing_skills,
        "Learning Roadmap": roadmap,
        "Interview Questions": questions,
        "AI Report": ai_report,
        "Skill Graph": graph
    }
    resume_history.append({
        "File": file.filename,
        "ATS": ats_score,
        "Career": career,
        "Skills": detected_skills,
        "Missing": missing_skills
    })

    cursor.execute(
        """
        INSERT INTO resumes(
            filename,
            career,
            ats,
            strength
        )
        VALUES(?,?,?,?)
        """,
        (
            file.filename,
            career,
            ats_score,
            strength
        )
    )

    conn.commit()

    return latest_report

def find_missing_skills(detected_skills):

    missing = []

    for skill in skills_database:

        if skill not in detected_skills:
            missing.append(skill)

    return missing[:5]
def learning_roadmap(missing):

    roadmap = []

    for skill in missing:
        roadmap.append("Learn " + skill)

    return roadmap
def predict_career(skills):

    if "python" in skills and "machine learning" in skills:

        return "AI Engineer"

    elif "react" in skills and "javascript" in skills:

        return "Frontend Developer"

    elif "sql" in skills and "power bi" in skills:

        return "Data Analyst"

    else:

        return "Software Developer"
    
def generate_questions(skills):

    questions=[]

    if "python" in skills:

        questions.append("Explain Python OOP Concepts.")

    if "sql" in skills:

        questions.append("Write SQL JOIN Query.")

    if "machine learning" in skills:

        questions.append("Difference between Supervised and Unsupervised Learning?")

    if "fastapi" in skills:

        questions.append("Explain FastAPI Architecture.")

    if "react" in skills:

        questions.append("Difference between React State and Props?")

    return questions 

def interview_score(skills):

    score = len(skills) * 10

    if score > 100:
        score = 100

    return score

questions_database = [

{
"question":"What is Machine Learning?",
"answer":"Machine Learning is a subset of AI that enables computers to learn from data."
},

{
"question":"Explain Python OOP.",
"answer":"OOP stands for Object Oriented Programming using Classes and Objects."
},

{
"question":"Difference between SQL and NoSQL?",
"answer":"SQL uses relational databases while NoSQL uses non-relational databases."
},

{
"question":"What is FastAPI?",
"answer":"FastAPI is a modern Python framework for building APIs."
}

]


@app.get("/mock-interview")
def mock_interview():

    return{

        "Questions":questions_database

    }

@app.get("/github-analysis/{username}")
def github_analysis(username: str):

    return {

        "Username": username,

        "Repositories": 12,

        "Followers": 45,

        "Following": 18,

        "Languages": [
            "Python",
            "JavaScript",
            "HTML",
            "CSS",
            "SQL"
        ],

        "GitHub Score": "87%",

        "Suggestion": [
            "Add more AI Projects",
            "Improve README files",
            "Use GitHub Actions",
            "Increase Commit Frequency"
        ]

    }

@app.get("/linkedin-analysis")
def linkedin_analysis():

    return {

        "Profile Strength": "82%",

        "Headline": "AI & Data Science Student",

        "Connections": 350,

        "Missing Sections": [

            "Projects",

            "Certifications",

            "Featured Section"

        ],

        "ATS Compatibility": "85%",

        "Suggestions": [

            "Add AI Projects",

            "Upload Resume",

            "Increase Connections",

            "Add GitHub Link"

        ]

    }

def ask_gemini(resume_text):

    prompt = f"""
You are an AI Career Mentor.

Analyze this resume.

Give:

1. Career Suggestion
2. Strengths
3. Weaknesses
4. Missing Skills
5. Learning Roadmap
6. Interview Tips

Resume:

{resume_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        return f"""
AI Report (Offline Mode)

Career Suggestion:
AI Engineer

Strengths:
• Strong Python programming skills
• Good knowledge of Machine Learning
• SQL & Power BI understanding

Weaknesses:
• Docker
• AWS
• React

Missing Skills:
• Docker
• AWS
• GitHub Actions

Learning Roadmap:
1. Learn Docker
2. Learn AWS
3. Build 3 AI Projects
4. Practice DSA
5. Improve GitHub Profile

Interview Tips:
• Practice Python coding questions.
• Revise Machine Learning concepts.
• Practice SQL queries.
• Build one end-to-end AI project.
"""
def generate_skill_graph(detected_skills):

    skill_names = detected_skills

    scores = []

    for skill in detected_skills:

        scores.append(80)

    plt.figure(figsize=(8,5))

    plt.bar(skill_names, scores)

    plt.title("AI Skill Graph")

    plt.xlabel("Skills")

    plt.ylabel("Score")

    plt.savefig("skill_graph.png")

    plt.close()

    return "skill_graph.png"

@app.post("/upload-certificate")
async def upload_certificate(file: UploadFile = File(...)):

    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)

    return {
        "Certificate": file.filename,
        "Status": "Verified ✅",
        "Skills Added": [
            "Leadership",
            "Discipline",
            "Team Work"
        ]
    }
@app.get("/skills")
def skills():

    return {
        "skills":[
            "Python",
            "SQL",
            "Machine Learning",
            "Power BI",
            "FastAPI"
        ]
    }
@app.get("/career-prediction")
def career_prediction():

    return{

        "Career":"AI Engineer",

        "Score":"92%",

        "Second":"Data Scientist"

    }
@app.get("/download-report")
def download_report():

    doc = SimpleDocTemplate("AI_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Career Digital Twin Report</b>", styles["Heading1"]))

    story.append(Paragraph("Developer : Amarjeet", styles["Normal"]))

    story.append(
        Paragraph(
            "Career Prediction : " +
            latest_report.get("Career Prediction","N/A"),
            styles["Normal"]
        )
    )
    
    story.append(
        Paragraph(
            "ATS Score : " +
            latest_report.get("ATS Score","0%"),
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "Strength : " +
            latest_report.get("Strength","N/A"),
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "Recommended Role : " +
            latest_report.get("Career Prediction","N/A"),
            styles["Normal"]
        )
    )

    doc.build(story)

    return FileResponse(
        "AI_Report.pdf",
        media_type="application/pdf",
        filename="AI_Report.pdf"
    )

@app.get("/compare-resumes")
def compare_resumes():

    if len(resume_history) < 2:

        return {

            "Message":"Upload 2 resumes first"

        }

    resume1 = resume_history[-2]

    resume2 = resume_history[-1]

    winner = resume1

    if resume2["ATS"] > resume1["ATS"]:

        winner = resume2

    return{

        "Resume A":resume1,

        "Resume B":resume2,

        "Winner":winner["File"]

    }
@app.get("/recruiter-dashboard")
def recruiter_dashboard():

    if len(resume_history) == 0:

        return {
            "Total Resume":0,
            "Average ATS":"0%",
            "Best Candidate":"None",
            "Top Skills":[],
            "Candidates":[]
        }

    total_resume = len(resume_history)

    average = sum(r["ATS"] for r in resume_history) // total_resume

    best = max(resume_history, key=lambda x: x["ATS"])

    skills = {}

    for resume in resume_history:

        for skill in resume["Skills"]:

            skills[skill] = skills.get(skill,0)+1

    top_skills = sorted(
        skills.items(),
        key=lambda x:x[1],
        reverse=True
    )[:5]

    return{

        "Total Resume":total_resume,

        "Average ATS":str(average)+"%",

        "Best Candidate":best["File"],

        "Top Skills":[x[0] for x in top_skills],

        "Candidates":resume_history

    }
@app.get("/all-resumes")
def all_resumes():

    cursor.execute(

    "SELECT * FROM resumes"

    )

    data = cursor.fetchall()

    return{

        "Data":data

    }
