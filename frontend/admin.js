const API = "http://127.0.0.1:5000";

// --------------------------------
// Load Everything
// --------------------------------

window.onload = () => {

    loadStats();
    loadUsers();
    loadAccounts();
    loadTransactions();
    loadFraudTransactions();

};

// --------------------------------
// Load Stats
// --------------------------------

async function loadStats(){

    const response =
    await fetch(`${API}/admin/stats`);

    const data =
    await response.json();

    document.getElementById("users")
    .innerText = data.users;

    document.getElementById("accounts")
    .innerText = data.accounts;

    document.getElementById("transactions")
    .innerText = data.transactions;

    document.getElementById("balance")
    .innerText =
    "₹" + data.total_balance;
}

// --------------------------------
// Load Users
// --------------------------------

async function loadUsers(){

    const response =
    await fetch(`${API}/admin/users`);

    const users =
    await response.json();

    let rows = "";

    users.forEach(user => {

        rows += `
        <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.password}</td>
        </tr>
        `;
    });

    document.querySelector(
    "#usersTable tbody"
    ).innerHTML = rows;
}

// --------------------------------
// Load Accounts
// --------------------------------

async function loadAccounts(){

    const response =
    await fetch(`${API}/admin/accounts`);

    const accounts =
    await response.json();

    let rows = "";

    accounts.forEach(account => {

        rows += `
        <tr>
            <td>${account.account_id}</td>
            <td>${account.user_id}</td>
            <td>${account.account_type}</td>
            <td>₹${account.balance}</td>
        </tr>
        `;
    });

    document.querySelector(
    "#accountsTable tbody"
    ).innerHTML = rows;
}

// --------------------------------
// Load Transactions
// --------------------------------

async function loadTransactions(){

    const response =
    await fetch(`${API}/admin/transactions`);

    const transactions =
    await response.json();

    let rows = "";

    transactions.forEach(tx => {

        rows += `
        <tr>
            <td>${tx.transaction_id}</td>
            <td>${tx.account_id}</td>
            <td>${tx.transaction_type}</td>
            <td>₹${tx.amount}</td>
            <td>${tx.transaction_time}</td>
        </tr>
        `;
    });

    document.querySelector(
    "#transactionsTable tbody"
    ).innerHTML = rows;
}

// --------------------------------
// Fraud Monitoring
// --------------------------------

async function loadFraudTransactions(){

    const response =
    await fetch(
        `${API}/admin/fraud-transactions`
    );

    const transactions =
    await response.json();

    let rows = "";

    transactions.forEach(tx => {

        let colorClass = "suspicious";

        if(
            tx.risk_level ===
            "High Risk Transaction"
        ){
            colorClass = "high";
        }

        rows += `
        <tr>
            <td>${tx.transaction_id}</td>
            <td>${tx.transaction_type}</td>
            <td>₹${tx.amount}</td>

            <td class="${colorClass}">
                ${tx.risk_level}
            </td>
        </tr>
        `;
    });

    document.querySelector(
        "#fraudTable tbody"
    ).innerHTML = rows;
}