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


## Workflow of the AI Smart Banking Application

You can explain the workflow in your project presentation like this:

### 1. User Registration

First, a new user opens the application and enters their **name, email, and password** in the registration page.

The frontend sends this information to the Flask backend using a **POST API request**. The backend validates the details and stores the user information in the **MySQL database**.

```text
User → Registration Page → Flask API → MySQL
```

### 2. User Login

After registration, the user logs in using their email and password.

The JavaScript frontend sends the login details to the Flask backend using the **Fetch API**. The backend verifies the credentials from MySQL. If they are valid, the user gets access to the banking dashboard.

```text
Login → Fetch API → Flask → MySQL → Authentication → Dashboard
```

### 3. Banking Operations

After login, the user can perform banking operations such as:

* Deposit money
* Withdraw money
* Check current balance
* View transaction history

When the user performs a transaction, JavaScript sends the transaction details to the Flask API. Flask processes the request and updates the corresponding information in MySQL.

```text
User Action
     ↓
JavaScript
     ↓
Flask REST API
     ↓
MySQL Database
     ↓
Updated Result
     ↓
Dashboard
```

### 4. Fraud Detection

For transactions, the system can use the **Machine Learning fraud detection model**.

The transaction information is passed to the trained **Random Forest model**. The model analyzes the transaction and determines its risk level, such as **Normal or suspicious**.

```text
Transaction
     ↓
ML Model
     ↓
Risk Prediction
     ↓
Normal / Suspicious
```

### 5. AI Financial Summary

The application also provides an AI-powered financial summary.

Transaction information is sent to the **Google Gemini API**, which analyzes the user's financial activity and generates a summary or recommendation.

```text
Transaction History
       ↓
Flask Backend
       ↓
Gemini AI
       ↓
Financial Summary
       ↓
Frontend
```

### 6. Complete Project Workflow

The complete workflow can be explained as:

```text
                 USER
                   ↓
          Frontend Interface
        HTML + CSS + JavaScript
                   ↓
              Fetch API
                   ↓
            Flask Backend
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
   MySQL Database       ML Fraud Model
        ↓                     ↓
   User/Account/        Risk Prediction
   Transactions              ↓
        └──────────┬──────────┘
                   ↓
              Gemini AI
                   ↓
        Financial Summary
                   ↓
             Dashboard
                   ↓
              USER
```

### Simple explanation 

> **"The workflow starts when the user registers and logs into the application. The frontend is developed using HTML, CSS, and JavaScript, and it communicates with the Flask backend through REST APIs using the Fetch API. Flask processes the user's requests and stores or retrieves information from the MySQL database. When a transaction is performed, the system records it in the database and the Machine Learning model analyzes the transaction to identify its risk level. The application also sends relevant transaction information to the Gemini API to generate AI-based financial summaries and recommendations. Finally, all results are displayed on the user's dashboard."**
