/* ================================
   COLLEGE ERP - JAVASCRIPT
================================ */

// Login form: sends a POST request to Flask instead of showing a fake success message.
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const role = document.getElementById("role").value;
        try {
            const response = await fetch('/api/login', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password, role})
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Login failed');
            sessionStorage.setItem('erpRole', result.role);
            sessionStorage.setItem('erpUsername', result.username);
            window.location.href = 'dashboard.html';
        } catch (error) { alert(error.message); }
    });
}

// Current year
const yearElements = document.querySelectorAll(".current-year");

yearElements.forEach(function (element) {
    element.textContent = new Date().getFullYear();
});

// Search table
const searchInput = document.getElementById("searchInput");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        const searchValue = this.value.toLowerCase();
        const tableRows = document.querySelectorAll("#dataTable tbody tr");

        tableRows.forEach(function (row) {
            row.style.display = row.textContent.toLowerCase().includes(searchValue)
                ? ""
                : "none";
        });
    });
}