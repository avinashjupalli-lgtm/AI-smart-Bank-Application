from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import joblib
import os
import google.generativeai as genai
from dotenv import load_dotenv

# -----------------------------
# Gemini Configuration
# -----------------------------
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

print("Gemini Initialized Successfully")

app = Flask(__name__)
CORS(app)
# -----------------------------
# Load Fraud Detection Model
# -----------------------------
model_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ML",
    "fraud_model.pkl"
)

fraud_model = joblib.load(model_path)

# -----------------------------
# Database Connection
# -----------------------------
import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT")),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )

# -----------------------------
# Home API
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "AI Banking Backend Running"
    })

# -----------------------------
# Register API
# -----------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE()")
        print("Current Database:", cursor.fetchone())
        cursor.execute("SHOW TABLES")
        print("Tables:", cursor.fetchall())

        query = """
        INSERT INTO users(name, email, password)
        VALUES(%s, %s, %s)
        """
        print("REGISTER DATA:", data)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (data["email"],)
        )
        existing = cursor.fetchone()
        if existing:
            return jsonify({
                "message": "User already exists"
            })
        cursor.execute(
            query,
            (
                data["name"],
                data["email"],
                data["password"]
            )
        )
        
        user_id = cursor.lastrowid
        cursor.execute("""
        INSERT INTO accounts
        (user_id, account_type, balance)
        VALUES (%s,%s,%s)
        """,
        (
            user_id,
            "Savings",
            0
        ))

        print("Rows affected:", cursor.rowcount)

        conn.commit()

        cursor.execute("SELECT * FROM users")
        print("ALL Users:", cursor.fetchall())

        cursor.close()
        conn.close()

        return jsonify({
            "message": "User Registered Successfully"
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# Login API
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM users
            WHERE email=%s AND password=%s
            """,
            (
                data["email"],
                data["password"]
            )
        )

        user = cursor.fetchone()

        if user:

            cursor.execute(
                """
                SELECT account_id
                FROM accounts
                WHERE user_id=%s
                """,
                (user["id"],)
            )

            account = cursor.fetchone()

            cursor.close()
            conn.close()

            return jsonify({
                "message": "Login Successful",
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "account_id": account["account_id"]
            })

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Invalid Credentials"
        }), 401

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
# -----------------------------
# Create Account API
# -----------------------------
@app.route("/create-account", methods=["POST"])
def create_account():
    try:
        data = request.get_json()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO accounts(
            user_id,
            account_type,
            balance
        )
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                data["user_id"],
                data["account_type"],
                0
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Account Created Successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# Deposit API
# -----------------------------
@app.route("/deposit", methods=["POST"])
def deposit():
    try:

        data = request.get_json()

        account_id = data["account_id"]
        amount = data["amount"]

        # -----------------------------
        # ML Fraud Prediction
        # -----------------------------
        prediction = fraud_model.predict([
            [
                amount,   # amount
                1,        # frequency
                amount,   # balance change
                12        # time
            ]
        ])[0]

        if prediction == 0:
            risk_level = "Normal Transaction"

        elif prediction == 1:
            risk_level = "Suspicious Transaction"

        else:
            risk_level = "High Risk Transaction"

        conn = get_connection()
        cursor = conn.cursor()

        # Update Balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_id = %s
            """,
            (amount, account_id)
        )

        # Save Transaction + Risk Level
        cursor.execute(
            """
            INSERT INTO transactions(
                account_id,
                transaction_type,
                amount,
                risk_level
            )
            VALUES(%s,%s,%s,%s)
            """,
            (
                account_id,
                "Deposit",
                amount,
                risk_level
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Deposit Successful",
            "risk_level": risk_level
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# Withdraw API
# -----------------------------
@app.route("/withdraw", methods=["POST"])
def withdraw():
    try:

        data = request.get_json()

        account_id = data["account_id"]
        amount = data["amount"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id=%s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if not account:
            return jsonify({
                "message": "Account Not Found"
            }), 404

        if account["balance"] < amount:
            return jsonify({
                "message": "Insufficient Balance"
            }), 400

        # -----------------------------
        # ML Fraud Prediction
        # -----------------------------
        prediction = fraud_model.predict([
            [
                amount,   # amount
                1,        # frequency
                amount,   # balance change
                12        # time
            ]
        ])[0]

        if prediction == 0:
            risk_level = "Normal Transaction"

        elif prediction == 1:
            risk_level = "Suspicious Transaction"

        else:
            risk_level = "High Risk Transaction"

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_id=%s
            """,
            (amount, account_id)
        )

        cursor.execute(
            """
            INSERT INTO transactions(
                account_id,
                transaction_type,
                amount,
                risk_level
            )
            VALUES(%s,%s,%s,%s)
            """,
            (
                account_id,
                "Withdraw",
                amount,
                risk_level
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Withdrawal Successful",
            "risk_level": risk_level
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
# -----------------------------
# Balance API
# -----------------------------
@app.route("/balance/<int:account_id>", methods=["GET"])
def balance(account_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id=%s
            """,
            (account_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# Transaction History API
# -----------------------------
@app.route("/transactions/<int:account_id>", methods=["GET"])
def transactions(account_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM transactions
            WHERE account_id=%s
            ORDER BY transaction_time DESC
            """,
            (account_id,)
        )

        history = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(history)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------
# Fraud Detection API
# -----------------------------
@app.route("/fraud-check", methods=["POST"])
def fraud_check():
    try:
        data = request.get_json()

        sample = [[
            data.get("amount", 0),
            data.get("frequency", 0),
            data.get("balance_change", 0),
            data.get("time", 0)
        ]]

        prediction = fraud_model.predict(sample)[0]

        risk_map = {
            0: "Normal",
            1: "Suspicious",
            2: "High Risk"
        }

        return jsonify({
            "risk": risk_map[prediction]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    #generate Summary API#
@app.route("/generate-summary/<int:account_id>", methods=["GET"])
def generate_summary(account_id):

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # -----------------------------
        # Get Account Balance
        # -----------------------------
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id=%s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if not account:

            cursor.close()
            conn.close()

            return jsonify({
                "error": "Account not found"
            }), 404

        balance = float(account["balance"])

        # -----------------------------
        # Get Transactions
        # -----------------------------
        cursor.execute(
            """
            SELECT
                transaction_type,
                amount,
                transaction_time
            FROM transactions
            WHERE account_id=%s
            ORDER BY transaction_time DESC
            """,
            (account_id,)
        )

        transactions = cursor.fetchall()

        cursor.close()
        conn.close()

        if not transactions:

            return jsonify({
                "summary":
                "No transactions found for this account."
            })

        # -----------------------------
        # Calculate Statistics
        # -----------------------------
        total_deposit = 0
        total_withdraw = 0

        transaction_text = ""

        for t in transactions:

            amount = float(t["amount"])

            if t["transaction_type"] == "Deposit":
                total_deposit += amount

            elif t["transaction_type"] == "Withdraw":
                total_withdraw += amount

            transaction_text += (
                f"{t['transaction_type']} "
                f"₹{amount} "
                f"on {t['transaction_time']}\n"
            )

        # -----------------------------
        # Random Forest Fraud Prediction
        # -----------------------------
        amount_feature = total_withdraw
        frequency_feature = len(transactions)
        balance_change_feature = abs(
            total_deposit - total_withdraw
        )
        time_feature = 12

        prediction = fraud_model.predict([
            [
                amount_feature,
                frequency_feature,
                balance_change_feature,
                time_feature
            ]
        ])[0]

        if prediction == 0:

            fraud_status = (
                "Normal Transaction"
            )

        elif prediction == 1:

            fraud_status = (
                "Suspicious Transaction"
            )

        else:

            fraud_status = (
                "High Risk Transaction"
            )

        print(
            "ML Fraud Result:",
            fraud_status
        )

        # -----------------------------
        # Gemini Prompt
        # -----------------------------
        prompt = f"""
You are an AI Banking Advisor.

Account Details:

Current Balance: ₹{balance}

Total Deposits: ₹{total_deposit}

Total Withdrawals: ₹{total_withdraw}

Number of Transactions:
{len(transactions)}

Machine Learning Fraud Detection Result:

{fraud_status}

Transaction History:

{transaction_text}

Analyze the account and provide:

1. Spending Analysis
2. Savings Behaviour
3. Financial Discipline Rating (out of 10)
4. Savings Recommendation
5. Explain the Machine Learning Fraud Detection Result
6. Fraud Risk Observation
7. Overall Financial Health Score (out of 10)

Keep the response professional.

Maximum 150 words.
"""

        response = gemini_model.generate_content(
            prompt
        )

        return jsonify({
            "summary": response.text,
            "fraud_prediction": fraud_status,
            "balance": balance,
            "total_deposits": total_deposit,
            "total_withdrawals": total_withdraw
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500    
 #database#

@app.route("/db-info")
def db_info():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE()")
    database = cursor.fetchone()

    cursor.execute("SELECT @@hostname, @@port")
    server = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({
        "database": database[0],
        "hostname": server[0],
        "port": server[1]
    })
@app.route("/all-users")
def all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users)
@app.route("/db-debug")
def db_debug():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE()")
    db = cursor.fetchone()

    cursor.execute("""
        SELECT TABLE_SCHEMA, TABLE_NAME
        FROM information_schema.tables
        WHERE TABLE_NAME='users'
    """)
    tables = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()

    return jsonify({
        "database": db,
        "tables": tables,
        "count": count
    })

@app.route("/connection-info")
def connection_info():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE()")
    db = cursor.fetchone()[0]

    cursor.execute("SELECT @@hostname")
    host = cursor.fetchone()[0]

    cursor.execute("SELECT @@port")
    port = cursor.fetchone()[0]

    return {
        "database": db,
        "hostname": host,
        "port": port
    }
@app.route("/admin-login", methods=["POST"])
def admin_login():

    try:

        data = request.get_json()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM admins
            WHERE username=%s
            AND password=%s
            """,
            (
                data["username"],
                data["password"]
            )
        )

        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin:
            return jsonify({
                "message":"Admin Login Successful"
            })

        return jsonify({
            "message":"Invalid Credentials"
        }),401

    except Exception as e:

        return jsonify({
            "error":str(e)
        }),500
@app.route("/admin/stats")
def admin_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )
    total_users = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM accounts"
    )
    total_accounts = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )
    total_transactions = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(balance) FROM accounts"
    )
    total_balance = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "users": total_users,
        "accounts": total_accounts,
        "transactions": total_transactions,
        "total_balance": float(total_balance or 0)
    })
@app.route("/admin/users")
def get_users():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM users
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users)
@app.route("/admin/accounts")
def get_accounts():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM accounts
    """)

    accounts = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(accounts)
@app.route("/admin/transactions")
def get_transactions():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM transactions
    ORDER BY transaction_time DESC
    """)

    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(transactions)
@app.route("/admin/fraud-transactions")
def fraud_transactions():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM transactions
    WHERE risk_level != 'Normal Transaction'
    ORDER BY transaction_time DESC
    """)

    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(transactions)
# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)