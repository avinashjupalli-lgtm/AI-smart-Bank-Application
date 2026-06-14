# 🏦 AI Banking System

An AI-powered Banking Application developed using Python, Flask, Machine Learning, HTML, CSS, and JavaScript. The system allows users to create accounts, perform deposits and withdrawals, view transaction history, generate AI-based financial summaries, and detect fraudulent transactions using a Machine Learning model.

---

## 🚀 Features

### 👤 User Management

* User Registration
* User Login Authentication
* Session Management
* User Dashboard

### 💰 Banking Operations

* Deposit Money
* Withdraw Money
* Check Account Balance
* Transaction History Tracking

### 🤖 AI Features

* AI-Based Financial Summary Generation
* Personalized Spending Analysis
* Savings Behaviour Analysis
* Financial Health Score

### 🛡️ Fraud Detection

* Machine Learning Fraud Prediction
* Risk Level Detection
* Normal vs Suspicious Transaction Classification
* Real-Time Fraud Analysis

### 👨‍💼 Admin Features

* View Registered Users
* Monitor Transactions
* Manage Banking Records

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Database

* MySQL

### Machine Learning

* Scikit-Learn
* Random Forest Classifier
* Pandas
* NumPy
* Joblib

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## 📂 Project Structure


AI-Banking-System/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── test_gemini.py
│   ├── routes/
│   └── ML/
│
├── frontend/
│   ├── index.html
│   ├── register.html
│   ├── admin.html
│   ├── style.css
│   ├── admin.css
│   ├── script.js
│   └── admin.js
│
├── ML/
│   ├── dataset.csv
│   ├── train_model.py
│   ├── test_model.py
│   ├── fraud_model.pkl
│   ├── confusion_matrix.png
│   └── evaluation.txt
│
├── requirements.txt
└── README.md

---

## ⚙️ Installation

### Clone Repository


git clone https://github.com/avinashjupalli-lgtm/AI-smart-Bank-Application
cd AI-Smart-Banking-System


### Create Virtual Environment

bash
python -m venv venv


### Activate Environment

#### Windows

bash
venv\Scripts\activate


#### Linux/Mac

bash
source venv/bin/activate


### Install Dependencies

bash
pip install -r requirements.txt


---

## ▶️ Run Backend

Navigate to backend folder:

bash
cd backend


Start Flask Server:

bash
python app.py


Server runs on:

text
http://127.0.0.1:5000


---

## ▶️ Run Frontend

Open:

text
frontend/index.html


or use VS Code Live Server.

Frontend runs on:

text
http://127.0.0.1:5500


---

## 🧠 Machine Learning Model

The fraud detection module is built using:

* Random Forest Classifier
* Transaction Amount
* Transaction Frequency
* Balance Change
* Transaction Time

Output:

* Normal Transaction
* Suspicious Transaction

Model file:

text
fraud_model.pkl


---

## 📊 Functional Modules

### Registration Module

Creates a new user account.

### Login Module

Authenticates registered users.

### Deposit Module

Allows users to add money to their account.

### Withdrawal Module

Allows users to withdraw funds.

### Transaction History Module

Stores and displays transaction records.

### Fraud Detection Module

Analyzes transactions and predicts fraud risk.

### AI Summary Module

Generates financial insights and recommendations.

---

## 🔒 Security Features

* Password Protection
* Session Management
* Fraud Detection Layer
* Input Validation
* API-Based Communication

---

## 📈 Future Enhancements

* OTP Verification
* Email Notifications
* Loan Recommendation System
* UPI Integration
* Cloud Deployment
* Advanced AI Analytics

---

## 👨‍💻 Author

**Jupalli Avinash**
**B.TECH-CSM**
**CMR TECHNICAL CAMPUS(CMRTC)**
GitHub:https://github.com/avinashjupalli-lgtm
Linkdin:https://www.linkedin.com/in/avinash-jupalli-bb2662291/

AI Banking System Project

Built using Flask, Machine Learning, HTML, CSS, and JavaScript.
