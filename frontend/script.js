const API = "http://127.0.0.1:5000";

let currentUser = null;
let accountId = 1; // Change later when login returns account_id

// ----------------------------
// Show Result
// ----------------------------
function show(data) {

    document.getElementById("result").innerHTML = `
        <h3>${data.message || ""}</h3>
        <p>Risk Level: ${data.risk_level || ""}</p>
    `;
}

// ----------------------------
// Register
// ----------------------------
async function register() {

    const response = await fetch(`${API}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    });

    const data = await response.json();

    alert(data.message || data.error);

    show(data);
}

// ----------------------------
// Login
// ----------------------------
async function login() {

    const response = await fetch(`${API}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: document.getElementById("loginEmail").value,
            password: document.getElementById("loginPassword").value
        })
    });

    const data = await response.json();

    if (data.message === "Login Successful") {
        accountId = data.account_id;
        currentUser = data;

        localStorage.setItem(
            "user",
            JSON.stringify(data)
        );

        document.getElementById("loginSection")
            .style.display = "none";

        document.getElementById("dashboard")
            .style.display = "block";

        document.getElementById("username")
            .innerText = data.name;

        loadBalance();
        loadTransactions();
        showSection(
    "dashboardSection"
);

        alert("Login Successful");
    }
    else {
        alert("Invalid Credentials");
    }

    show(data);
}

// ----------------------------
// Logout
// ----------------------------
function logout() {

    localStorage.clear();

    location.reload();
}

// ----------------------------
// Deposit
// ----------------------------
async function deposit() {

    const amount =
        Number(
            document.getElementById(
                "depositAmount"
            ).value
        );

    const response = await fetch(
        `${API}/deposit`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                account_id: accountId,
                amount: amount
            })
        }
    );

    const data = await response.json();


    alert(
    data.message +
    "\nRisk Level: " +
    data.risk_level
    );


    loadBalance();
    loadTransactions();

    show(data);
}

// ----------------------------
// Withdraw
// ----------------------------
async function withdrawMoney() {

    const amount =
        Number(
            document.getElementById(
                "withdrawAmount"
            ).value
        );

    const response = await fetch(
        `${API}/withdraw`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                account_id: accountId,
                amount: amount
            })
        }
    );

    const data = await response.json();

    
    alert(
    data.message +
    "\nRisk Level: " +
    data.risk_level
    );

    loadBalance();
    loadTransactions();

    show(data);
}

// ----------------------------
// Load Balance
// ----------------------------
async function loadBalance() {

    const response =
        await fetch(
            `${API}/balance/${accountId}`
        );

    const data =
        await response.json();

    document.getElementById(
        "balanceCard"
    ).innerText =
        "₹" + data.balance;
}

// ----------------------------
// Load Transactions
// ----------------------------
async function loadTransactions() {

    const response =
        await fetch(
            `${API}/transactions/${accountId}`
        );

    const data =
        await response.json();

    let rows = "";

    let deposits = 0;
    let withdrawals = 0;

    data.forEach(tx => {

        if (
            tx.transaction_type ===
            "Deposit"
        ) {
            deposits +=
                parseFloat(tx.amount);
        }

        if (
            tx.transaction_type ===
            "Withdraw"
        ) {
            withdrawals +=
                parseFloat(tx.amount);
        }

        rows += `
        <tr>
            <td>${tx.transaction_id}</td>
            <td>${tx.transaction_type}</td>
            <td>₹${tx.amount}</td>
            <td>${tx.transaction_time}</td>
        </tr>
        `;
    });

    document.querySelector(
        "#historyTable tbody"
    ).innerHTML = rows;

    document.getElementById(
        "depositCard"
    ).innerText =
        "₹" + deposits;

    document.getElementById(
        "withdrawCard"
    ).innerText =
        "₹" + withdrawals;
}

// ----------------------------
// Fraud Check
// ----------------------------
async function fraudCheck() {

    const response = await fetch(
        `${API}/fraud-check`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                amount: Number(
                    document.getElementById(
                        "amount"
                    ).value
                ),
                frequency: Number(
                    document.getElementById(
                        "frequency"
                    ).value
                ),
                balance_change: Number(
                    document.getElementById(
                        "balance_change"
                    ).value
                ),
                time: Number(
                    document.getElementById(
                        "time"
                    ).value
                )
            })
        }
    );

    const data =
        await response.json();

    alert(
        "Risk Level: " +
        data.risk
    );

    show(data);
}

// ----------------------------
// Generate Summary
// ----------------------------
async function generateSummary() {

    const response =
        await fetch(
            `${API}/generate-summary/${accountId}`
        );

    const data =
        await response.json();

    document.getElementById(
        "summaryResult"
    ).innerText =
        data.summary;

    show(data);
}

// ----------------------------
// Auto Login
// ----------------------------
window.onload = () => {

    const user =
        JSON.parse(
            localStorage.getItem(
                "user"
            )
        );

    if (user) {

        currentUser = user;
        accountId = user.account_id;

        document.getElementById(
            "loginSection"
        ).style.display = "none";

        document.getElementById(
            "dashboard"
        ).style.display = "block";

        document.getElementById(
            "username"
        ).innerText =
            user.name;

        loadBalance();
        loadTransactions();

        showSection(
            "dashboardSection"
        );

    }
};

function showSection(id) {

    const sections =
        document.querySelectorAll(".content-section");

    sections.forEach(section => {
        section.style.display = "none";
    });

    const selected =
        document.getElementById(id);

    if(selected){
        selected.style.display = "block";
    }

    console.log("Showing:", id);
}