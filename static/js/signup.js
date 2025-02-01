
    const form = document.getElementById('signupForm');
    const errorMessage = document.getElementById('errorMessage');
    const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const submitData =  async (e) => {
            e.preventDefault()

            form.addEventListener('submit', async () => {
        

        console.log(username , email,password)

        try {
            const response = await fetch('/contact-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                form.reset();
            } else {
                errorMessage.textContent = result.message || "Something went wrong!";
            }
        } catch (error) {
            errorMessage.textContent = "An error occurred. Please try again later.";
        }
    });

        }