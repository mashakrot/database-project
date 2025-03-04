document.getElementById('loginButton').addEventListener('click', async function(event) {
    event.preventDefault();

    const email = document.getElementById('input-email').value;
    const password = document.getElementById('input-password').value;

    try {
        const response = await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Login successful:", data);
            alert("Login successful!");
        } else {
            console.log("Error:", data.message);
            alert("Invalid credentials");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Server error. Please try again later.");
    }
});
