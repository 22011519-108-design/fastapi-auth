const BASE_URL = "http://127.0.0.1:8000/library";

const output = document.getElementById("output");

// ================= SEARCH =================

async function searchBooks() {

    const query = document.getElementById("search_query").value;

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

        output.textContent = JSON.stringify(data, null, 4);

    } catch (error) {

        output.textContent = error;

    }

}


// ================= CHECK =================

async function checkAvailability() {

    const book_id = parseInt(
        document.getElementById("check_book_id").value
    );

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

        output.textContent = JSON.stringify(data, null, 4);

    } catch (error) {

        output.textContent = error;

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

    try {

        const response = await fetch(`${BASE_URL}/borrow`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: user_id,
                book_id: book_id
            })
        });

        const data = await response.json();

        output.textContent = JSON.stringify(data, null, 4);

    } catch (error) {

        output.textContent = error;

    }

}


// ================= RETURN =================

async function returnBook() {

    const loan_id = parseInt(
        document.getElementById("return_loan_id").value
    );

    try {

        const response = await fetch(`${BASE_URL}/return`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                loan_id: loan_id
            })
        });

        const data = await response.json();

        output.textContent = JSON.stringify(data, null, 4);

    } catch (error) {

        output.textContent = error;

    }

}