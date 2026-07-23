// ================= Resume Analysis =================

async function analyzeResume() {

    const fileInput = document.getElementById("resumeFile");

    if (fileInput.files.length === 0) {
        alert("Please Select Resume");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("http://127.0.0.1:9000/analyze-resume", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `

    <h2>AI Resume Analysis</h2>

    <b>ATS Score :</b> ${data["ATS Score"]}<br><br>

    <b>Career :</b> ${data["Career Prediction"]}<br><br>

    <b>Strength :</b> ${data["Strength"]}<br><br>

    <b>Detected Skills :</b>
    ${data["Detected Skills"].join(", ")}
    <br><br>

    <b>Missing Skills :</b>
    ${data["Missing Skills"].join(", ")}
    <br><br>

    <b>Interview Questions :</b>

    <ul>
    ${data["Interview Questions"].map(q => `<li>${q}</li>`).join("")}
    </ul>

    <b>Interview Score :</b>
    ${data["Interview Score"]}<br><br>

    <b>AI Report</b>

    <pre>${data["AI Report"]}</pre>

    `;
    document.getElementById("twinCareer").innerHTML =
        data["Career Prediction"];

    document.getElementById("twinStrength").innerHTML =
        data["Strength"];

    document.getElementById("twinSkills").innerHTML =
        data["Detected Skills"].join(", ");

    drawSkillChart(data["Detected Skills"]);

    document.getElementById("totalResume").innerHTML = "1";

    document.getElementById("averageATS").innerHTML =
        data["ATS Score"];

    document.getElementById("bestCandidate").innerHTML =
        data["Career Prediction"];

    document.getElementById("topSkills").innerHTML =
        data["Detected Skills"].slice(0,3).join(", ");

    document.getElementById("hiringStatus").innerHTML =
        data["ATS Score"] >= "70%" ? "Hire ✅" : "Need Improvement";

    updateATS(data["ATS Score"]);

    updateDashboardCards(data);

    updateDigitalTwin(data);

}


// ================= Certificate Upload =================

async function uploadCertificate(){

    const file = document.getElementById("certificateFile");

    if(file.files.length == 0){

        alert("Select Certificate");

        return;
    }

    const formData = new FormData();

    formData.append("file", file.files[0]);

    const response = await fetch("http://127.0.0.1:9000/upload-certificate",{

        method:"POST",

        body:formData

    });

    const data = await response.json();
    document.getElementById("cardCertificate").innerHTML = "1";

    document.getElementById("certificateResult").innerHTML =

    "<b>Status :</b> " + data.Status +

    "<br><b>Skills :</b> " + data["Skills Added"].join(", ");

}



// ================= Show Skills =================

async function showSkills(){

    const response = await fetch("http://127.0.0.1:9000/skills");

    const data = await response.json();

    document.getElementById("skills").innerHTML = data.skills.join("<br>");

}



// ================= Career Prediction =================

async function careerPrediction(){

    const response = await fetch("http://127.0.0.1:9000/career-prediction");

    const data = await response.json();

    document.getElementById("career").innerHTML =

    "<b>" + data.Career + "</b><br>" +

    "Score : " + data.Score;

}
let chart = null;

function drawSkillChart(skills){

    const canvas = document.getElementById("skillChart");

    if(chart){
        chart.destroy();
    }

    chart = new Chart(canvas,{

        type:"bar",

        data:{

            labels:skills,

            datasets:[{

                label:"Detected Skills",

                data:skills.map(()=>90),

                backgroundColor:[
                    "#4CAF50",
                    "#2196F3",
                    "#FFC107",
                    "#9C27B0",
                    "#FF5722",
                    "#00BCD4",
                    "#795548",
                    "#3F51B5"
                ]

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            scales:{
                y:{
                    beginAtZero:true,
                    max:100
                }
            }

        }

    });

}
function updateATS(score){

    score = parseInt(score);

    document.getElementById("atsProgress").style.width = score + "%";

    document.getElementById("atsText").innerHTML = score + "%";

}
function updateDashboardCards(data){

    document.getElementById("cardATS").innerHTML =
        data["ATS Score"];

    document.getElementById("cardSkills").innerHTML =
        data["Detected Skills"].length;

    document.getElementById("cardCareer").innerHTML =
        data["Career Prediction"];

}
function updateDigitalTwin(data){

    document.getElementById("currentCareer").innerHTML =
        data["Career Prediction"];

    document.getElementById("careerReadiness").innerHTML =
        data["ATS Score"];

    document.getElementById("skillGap").innerHTML =
        data["Missing Skills"].length + " Skills";

}
function downloadReport(){

    window.open("http://127.0.0.1:9000/download-report");

}
async function startInterview(){

    const response =
    await fetch("http://127.0.0.1:9000/mock-interview");

    const data =
    await response.json();

    let html="";

    data.Questions.forEach((q,index)=>{

        html+=`

        <h3>Question ${index+1}</h3>

        <p>${q.question}</p>

        <textarea
        rows="3"
        style="width:95%"
        placeholder="Write Answer Here">
        </textarea>

        <hr>

        `;

    });

    html+=`

    <button onclick="alert('Demo Version')">

    Submit Interview

    </button>

    `;

    document.getElementById("interviewBox").innerHTML=html;

}

async function analyzeGithub(){

    const username =
    document.getElementById("githubUsername").value;

    if(username==""){

        alert("Enter GitHub Username");

        return;

    }

    const response =
    await fetch(
    "http://127.0.0.1:9000/github-analysis/"+username
    );

    const data =
    await response.json();

    document.getElementById("githubResult").innerHTML=`

    <h3>${data.Username}</h3>

    Repositories :
    ${data.Repositories}
    <br><br>

    Followers :
    ${data.Followers}
    <br><br>

    Following :
    ${data.Following}
    <br><br>

    Languages :

    ${data.Languages.join(", ")}

    <br><br>

    GitHub Score :

    ${data["GitHub Score"]}

    <br><br>

    Suggestion :

    <ul>

    ${data.Suggestion.map(s=>`<li>${s}</li>`).join("")}

    </ul>

    `;

}

async function analyzeLinkedIn(){

    const response =
    await fetch("http://127.0.0.1:9000/linkedin-analysis");

    const data =
    await response.json();

    document.getElementById("linkedinResult").innerHTML = `

    <h3>Profile Strength :
    ${data["Profile Strength"]}</h3>

    <p>

    <b>Headline :</b>

    ${data.Headline}

    </p>

    <p>

    <b>Connections :</b>

    ${data.Connections}

    </p>

    <p>

    <b>ATS :</b>

    ${data["ATS Compatibility"]}

    </p>

    <b>Missing Sections</b>

    <ul>

    ${data["Missing Sections"].map(x=>`<li>${x}</li>`).join("")}

    </ul>

    <b>Suggestions</b>

    <ul>

    ${data.Suggestions.map(x=>`<li>${x}</li>`).join("")}

    </ul>

    `;

}

function toggleTheme(){

    document.body.classList.toggle("dark");

    const btn=document.getElementById("themeBtn");

    if(document.body.classList.contains("dark")){

        btn.innerHTML="☀ Light Mode";

    }

    else{

        btn.innerHTML="🌙 Dark Mode";

    }

}

async function compareResume(){

    const response =
    await fetch("http://127.0.0.1:9000/compare-resumes");

    const data =
    await response.json();

    if(data.Message){

        document.getElementById("comparisonResult").innerHTML =
        data.Message;

        return;
    }

    document.getElementById("comparisonResult").innerHTML =

    `
    <h3>Resume A</h3>

    ATS :
    ${data["Resume A"].ATS}%<br>

    Career :
    ${data["Resume A"].Career}<br><br>

    <h3>Resume B</h3>

    ATS :
    ${data["Resume B"].ATS}%<br>

    Career :
    ${data["Resume B"].Career}<br><br>

    🏆 Winner :
    <b>${data["Winner"]}</b>
    `;
}
async function showDatabase(){

    const response =
    await fetch("http://127.0.0.1:9000/all-resumes");

    const data =
    await response.json();

    let html="";

    data.Data.forEach(r=>{

        html+=`

        <p>

        ${r[1]}

        |

        ${r[2]}

        |

        ${r[3]}%

        </p>

        `;

    });

    document.getElementById("database").innerHTML=html;

}