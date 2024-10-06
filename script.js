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
