// Sign up page dynamic interactions
function openSignupModal() {
	document.getElementById("login-modal").style.display = "none";
	document.getElementById("signup-modal").style.display = "block";
}

function openLoginModal() {
	document.getElementById("signup-modal").style.display = "none";
	document.getElementById("login-modal").style.display = "block";
}

document.addEventListener('DOMContentLoaded', function() {
	const signupBtn = document.getElementById('signupBtn');
	const loginBtn = document.getElementById('loginBtn');
	const signupModal = document.getElementById('signup-modal');
	const loginModal = document.getElementById('login-modal');
	const signupClose = signupModal.querySelector('.close-button');
	const loginClose = loginModal.querySelector('.close-button');

	if (signupBtn) {
		signupBtn.onclick = function() {
			signupModal.style.display = 'block';
		};
	}

	if (loginBtn) {
		loginBtn.onclick = function() {
			loginModal.style.display = 'block';
		};
	}

	if (signupModal && signupClose) {
		signupClose.onclick = function () {
			signupModal.style.display = 'none';
		};

		window.addEventListener('click', function(event) {
			if (event.target == signupModal) {
				signupModal.style.display = 'none';
			}
		});
	}

	if (loginModal && loginClose) {
		loginClose.onclick = function () {
			loginModal.style.display = 'none';
		};

		window.addEventListener('click', function(event) {
			if (event.target == loginModal) {
				loginModal.style.display = 'none';
			}
		});
	}

	document.getElementById("signup-form").onsubmit = function(e) {
		e.preventDefault();

		// Signup logic to send data to server/database
		window.location.href = document.referrer;
	}

	document.getElementById("login-form").onsubmit = function(e) {
		e.preventDefault();

		// Signup logic to send data to server/database
		window.location.href = document.referrer;
	};
});

document.getElementById('signup-form').addEventListener('submit', function(event) {
	event.preventDefault();


	const email = document.getElementById('signup-email').value.trim();
	const password = document.getElementById('signup-password').value.trim();
	const confirmPassword = document.getElementById('confirm-password').value.trim();


	fetch("{% url 'signUp' %}", {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
		},
		body: JSON.stringify({
			'signup-email': email,
			'signup-password': password,
			'confirm-password': confirmPassword
		})
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				window.location.href = data.redirect_url;
			} else {
				for (let error in data.errors) {
					const errorMessage = document.createElement('p');
					errorMessage.textContent = data.errors[error];
				}
			}
		});
});

// Function to handle the sign-in form submission
document.getElementById('login-form').addEventListener('submit', function(event) {
	event.preventDefault();


	const email = document.getElementById('login-email').value.trim();
	const password = document.getElementById('login-password').value.trim();

	fetch("{% url 'signIn' %}", {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
		},
		body: JSON.stringify({
			'login-email': email,
			'login-password': password
		})
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				window.location.href = data.redirect_url;
			} else {
				for (let error in data.errors) {
					const errorMessage = document.createElement('p');
					errorMessage.textContent = data.errors[error];
				}
			}
		});
});

// Function to handle sign-out
document.getElementById('signOutButton').addEventListener('click', function() {
	// Send request to log the user out
	fetch("{% url 'signout' %}", {
		method: 'POST',
		headers: {
			'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
		}
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				window.location.href = data.redirect_url; // Redirect to home page
			}
		});
});
