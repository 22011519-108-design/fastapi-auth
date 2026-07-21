const BASE_URL = "http://127.0.0.1:8000/library";

const output = document.getElementById("output");

// ================= DASHBOARD STATS =================

async function loadDashboardStats() {

    try {

        const response = await fetch(`${BASE_URL}/stats`);

        const data = await response.json();

        document.getElementById("totalBooks").textContent =
        data.total_books;

        document.getElementById("totalUsers").textContent =
        data.total_users;

        document.getElementById("borrowedBooks").textContent =
        data.borrowed_books;

        document.getElementById("availableBooks").textContent =
        data.available_books;

    }

    catch(error){

        console.error("Dashboard Error:", error);

    }

}

// ================= SEARCH =================

async function searchBooks() {

    const query = document.getElementById("search_query").value;

    const tbody = document.getElementById("resultsBody");

    tbody.innerHTML = `
        <tr>
            <td colspan="5">Searching...</td>
        </tr>
    `;

    try {

        const response = await fetch(`${BASE_URL}/search`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query
            })
        });

        const data = await response.json();

        const books = data.books;

        tbody.innerHTML = "";

        if (!books || books.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="5">No books found.</td>
                </tr>
            `;

            return;

        }

        books.forEach(book => {

            tbody.innerHTML += `
                <tr>

                    <td>${book.id}</td>

                    <td>${book.title}</td>

                    <td>${book.author}</td>

                    <td>${book.genre}</td>

                    <td>
                        <span class="badge ${book.available_copies > 0 ? "available" : "unavailable"}">
                            ${book.available_copies}
                        </span>
                    </td>

                </tr>
            `;

        });

        document.getElementById("output").textContent = data.message;

    }

    catch(error){

        console.error(error);

        tbody.innerHTML = `
            <tr>
                <td colspan="5">
                    Something went wrong.
                </td>
            </tr>
        `;

    }

}

// ================= CHECK =================

async function checkAvailability() {

    const book_id = parseInt(
        document.getElementById("check_book_id").value
    );

    const result = document.getElementById("availabilityResult");

    if (isNaN(book_id)) {

        result.innerHTML = `
            <div class="error-box">
                Please enter a valid Book ID.
            </div>
        `;

        return;
    }

    result.innerHTML = `
        <div class="loading">
            Checking availability...
        </div>
    `;

    try {

        const response = await fetch(`${BASE_URL}/check`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                book_id: book_id
            })

        });

        const data = await response.json();

        if (!data.available && !data.title) {

            result.innerHTML = `
                <div class="error-box">
                    Book not found.
                </div>
            `;

            return;
        }

        result.innerHTML = `

            <div class="book-card">

                <h3>${data.title}</h3>

                <p><strong>Book ID:</strong> ${data.book_id}</p>

                <p><strong>Available Copies:</strong> ${data.available_copies}</p>

                <p>

                    <strong>Status:</strong>

                    <span class="badge ${data.available ? "available" : "unavailable"}">

                        ${data.available ? "Available" : "Unavailable"}

                    </span>

                </p>

            </div>

        `;

    }

    catch(error){

        console.error(error);

        result.innerHTML = `
            <div class="error-box">
                Server Error
            </div>
        `;

    }

}

// ================= BORROW =================

async function borrowBook() {

    const user_id = parseInt(
        document.getElementById("borrow_user_id").value
    );

    const book_id = parseInt(
        document.getElementById("borrow_book_id").value
    );

    const result = document.getElementById("borrowResult");

    result.innerHTML = "Processing...";

    try {

        const response = await fetch(`${BASE_URL}/borrow`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                user_id,
                book_id
            })

        });

        const data = await response.json();

        if (data.success) {

            result.innerHTML = `
                <div class="success">
                    ✅ ${data.message}<br><br>
                    <strong>Loan ID:</strong> ${data.loan_id}<br>
                    <strong>Book:</strong> ${data.book}<br>
                    <strong>Due Date:</strong> ${new Date(data.due_date).toLocaleDateString()}
                </div>
            `;

        } else {

            result.innerHTML = `
                <div class="error">
                    ❌ ${data.message}
                </div>
            `;

        }

        loadDashboardStats();

        if (document.getElementById("search_query").value.trim() !== "") {
            searchBooks();
        }

    }

    catch (error) {

        console.error(error);

        result.innerHTML = `
            <div class="error">
                Server Error
            </div>
        `;

    }

}

// ================= RETURN =================

async function returnBook() {

    const loan_id = parseInt(
        document.getElementById("return_loan_id").value
    );

    const result = document.getElementById("returnResult");

    result.innerHTML = "Processing...";

    try {

        const response = await fetch(`${BASE_URL}/return`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                loan_id
            })

        });

        const data = await response.json();

        if (data.success) {

            result.innerHTML = `
                <div class="success">
                    ✅ ${data.message}<br><br>
                    <strong>Book:</strong> ${data.book}
                </div>
            `;

        } else {

            result.innerHTML = `
                <div class="error">
                    ❌ ${data.message}
                </div>
            `;

        }

        // Refresh dashboard
        loadDashboardStats();

        // Refresh search table
        if (document.getElementById("search_query").value.trim() !== "") {
            searchBooks();
        }

    }

    catch (error) {

        console.error(error);

        result.innerHTML = `
            <div class="error">
                Server Error
            </div>
        `;

    }

}

loadStats();
loadDashboardStats();