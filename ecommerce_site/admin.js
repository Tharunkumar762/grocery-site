const API_BASE_URL = "/api";

function adminLogin() {
    fetch(`${API_BASE_URL}/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = "admin_dashboard.html";
        } else {
            document.getElementById("error").innerText = "Invalid admin credentials";
        }
    });
}

/* LOAD USERS */
if (document.getElementById("usersTable")) {
    fetch(`${API_BASE_URL}/admin/users`)
    .then(res => res.json())
    .then(users => {
        const table = document.getElementById("usersTable");
        users.forEach(u => {
            table.innerHTML += `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.username}</td>
                    <td>${u.email}</td>
                </tr>
            `;
        });
    });

    fetch(`${API_BASE_URL}/admin/orders`)
    .then(res => res.json())
    .then(orders => {
        const table = document.getElementById("ordersTable");
        orders.forEach(o => {
            table.innerHTML += `
                <tr>
                    <td>${o.id}</td>
                    <td>${o.username}</td>
                    <td>${o.product}</td>
                    <td>${o.status}</td>
                    <td>
                        ${o.status === "Pending"
                        ? `<button class="approve-btn" onclick="approve(${o.id})">Approve</button>`
                        : "✔"}
                    </td>
                </tr>
            `;
        });
    });
}

function approve(id) {
    fetch(`${API_BASE_URL}/admin/order/approve`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ order_id: id })
    })
    .then(() => location.reload());
}
