// Sign up page dynamic interactions
function openSignupModal() {
  document.getElementById("signup-modal").style.display = "block";
}

function openLoginModal() {
  document.getElementById("login-modal").style.display = "block";
}

document.addEventListener('DOMContentLoaded', function() {
  const signupBtn = document.getElementById('signupBtn');
	const loginBtn = document.getElementById('loginBtn');
	const signupModal = document.getElementById('signup-modal');
	const loginModal = document.getElementById('login-modal');
	const span = document.getElementsByClassName('close-button')[0];

	if (signupBtn) {
		signupBtn.onclick = function() {
			signupModal.style.display = 'block';
		};
	}

	if (signupModal && span) {
		span.onclick = function () {
			signupModal.style.display = 'none';
		}

		window.onclick = function(event) {
			if (event.target == signupModal) {
				signupModal.style.display = 'none';
			}
		}

		document.getElementById("signup-form").onsubmit = function(e) {
			e.preventDefault();

			// Signup logic to send data to server/database
			window.location.href = document.referrer;
		}
	}

	if (loginBtn) {
		loginBtn.onclick = function() {
			loginModal.style.display = 'block';
		};
	}

	if (loginModal && span) {
		span.onclick = function () {
			loginModal.style.display = 'none';
		}

		window.onclick = function(event) {
			if (event.target == loginModal) {
				loginModal.style.display = 'none';
			}
		}

		document.getElementById("login-form").onsubmit = function(e) {
			e.preventDefault();

			// Signup logic to send data to server/database
			window.location.href = document.referrer;
		}
	}
});
