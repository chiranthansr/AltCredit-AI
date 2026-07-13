// api.js

// BACKEND DEV: Change this to your live server URL (e.g., http://localhost:5000/api)
const BASE_URL = "http://127.0.0.1:8000";

// Helper to get JWT token for authenticated requests
const getAuthHeaders = () => {
    const token = localStorage.getItem('jwt_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

// Screen 1: Register
async function handleRegister(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {

        const response = await fetch(`${BASE_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {

            alert("Registration Successful");

            window.location.href = "login.html";

        } else {

            alert(result.detail || result.message);

        }

    } catch (error) {

        console.error(error);

        alert("Server Error");

    }
}

// Screen 2: Login
async function handleLogin(event) {
    event.preventDefault();

    const data = Object.fromEntries(new FormData(event.target).entries());

    try {

        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {

            // Save user information
            localStorage.setItem("email", result.user.email);
            localStorage.setItem("full_name", result.user.full_name);
            localStorage.setItem("user_type", result.user.user_type);

            alert(result.message);

            window.location.href = "consent.html";

        } else {

            alert(result.detail);

        }

    } catch (error) {

        console.error(error);

        alert("Server Error");

    }
}

// Screen 3: Consent
async function handleConsent(event) {
    event.preventDefault();

    const data = {
        email: localStorage.getItem("email"),

        bank_access: document.getElementById("bank").checked,

        location_access: document.getElementById("location").checked,

        questionnaire_access: document.getElementById("questionnaire").checked
    };

    try {

        const response = await fetch("http://127.0.0.1:8000/consent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if(response.ok){
            alert(result.message);
            window.location.href = "credit.html";
        }
        else{
            alert(result.detail);
        }

    }
    catch(error){
        console.error(error);
        alert("Server Error");
    }
}

// Screen 4: Credit Info
async function handleCreditInfo(event) {

    event.preventDefault();

    const formData = new FormData(event.target);

    const data = {
        email: localStorage.getItem("email")
    };

    formData.forEach((value, key) => {
        data[key] = Number(value);
    });

    try {

        const response = await fetch(`${BASE_URL}/credit-input`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {

            alert(result.message);

            window.location.href = "quiz.html";

        } else {

            alert(result.detail);

        }

    } catch (error) {

        console.error(error);

        alert("Server Error");

    }

}

// Screen 5: Quiz
async function handleQuiz(event) {

    event.preventDefault();

    const formData = new FormData(event.target);

    const answers = Object.fromEntries(formData.entries());

    let score = 0;

    // Question 1
    if (answers.q1 === "B") score += 3;
    else if (answers.q1 === "C") score += 2;
    else if (answers.q1 === "A") score += 1;
    else score += 0;

    // Question 2
    if (answers.q2 === "A") score += 3;
    else if (answers.q2 === "B") score += 2;
    else score += 1;

    // Question 3
    if (answers.q3 === "A") score += 3;
    else if (answers.q3 === "C") score += 2;
    else score += 1;

    let risk_level;

    if (score >= 8)
        risk_level = "Low";
    else if (score >= 5)
        risk_level = "Medium";
    else
        risk_level = "High";

    const data = {
        email: localStorage.getItem("email"),
        quiz_score: score,
        risk_level: risk_level
    };

    try {

        const response = await fetch(`${BASE_URL}/questionnaire`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {

            alert(result.message);

            window.location.href = "generate.html";

        } else {

            alert(result.detail);

        }

    } catch (error) {

        console.error(error);

        alert("Server Error");

    }

}

// Screen 6: Generate Score
async function handleGenerateScore() {

    const data = {
        email: localStorage.getItem("email")
    };

    try {

        const response = await fetch(`${BASE_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {

            alert("Credit Score Generated Successfully!");

            window.location.href = "dashboard.html";

        } else {

            alert(result.detail);

        }

    } catch (error) {

        console.error(error);

        alert("Server Error");

    }

}

// Screen 7: Fetch Dashboard Data
// Screen 7: Fetch Dashboard Data
async function fetchDashboardData() {
    try {

        const email = localStorage.getItem("email");

        const response = await fetch(`${BASE_URL}/dashboard/${email}`);

        const userData = await response.json();

        document.getElementById('display_name').innerText = userData.full_name;
        document.getElementById('display_score').innerText = userData.prediction.credit_score;
        document.getElementById('display_risk').innerText = userData.prediction.risk_level;
        document.getElementById('display_decision').innerText = userData.prediction.loan_decision;
        document.getElementById('display_approval').innerText = userData.prediction.approval_probability;
        document.getElementById('display_default').innerText = userData.prediction.default_probability;

        const explanationsList = document.getElementById('display_explanations');
        explanationsList.innerHTML = '';

        userData.prediction.explanations.forEach(explanation => {
            const li = document.createElement('li');
            li.innerText = explanation;
            explanationsList.appendChild(li);
        });

    } catch (error) {
        console.error(error);
    }
}