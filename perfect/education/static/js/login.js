
        // Form Validation
        const loginForm = document.getElementById('loginForm');

        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Clear previous errors
            document.getElementById('usernameError').innerText = '';
            document.getElementById('emailError').innerText = '';
            document.getElementById('passwordError').innerText = '';

            let isValid = true;

            // Validate Username
            const username = document.getElementById('username').value.trim();
            if (username === '') {
                isValid = false;
                document.getElementById('usernameError').innerText = 'Username is required.';
            }

            // Validate Email
            const email = document.getElementById('email').value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (email === '') {
                isValid = false;
                document.getElementById('emailError').innerText = 'Email is required.';
            } else if (!emailRegex.test(email)) {
                isValid = false;
                document.getElementById('emailError').innerText = 'Enter a valid email address.';
            }

            // Validate Password
            const password = document.getElementById('password').value.trim();
            if (password === '') {
                isValid = false;
                document.getElementById('passwordError').innerText = 'Password is required.';
            } else if (password.length < 6) {
                isValid = false;
                document.getElementById('passwordError').innerText = 'Password must be at least 6 characters.';
            }

            // If all validations pass, submit the form (simulate for now)
          if (isValid) {
                alert('Login successful!');
            }
        });
   