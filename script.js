// Sign up page dynamic interactions
document.addEventListener('DOMContentLoaded', function() {
  const signupBtn = document.getElementById('signupBtn');
	const modal = document.getElementById('signup-modal');
	const span = document.getElementsByClassName('close-button')[0];

	if (signupBtn) {
		signupBtn.onclick = function() {
			// window.location.href = 'signup.html';
			modal.style.display = 'block';
		};
	}

	if (modal && span) {
		span.onclick = function () {
			// window.location.href = document.referrer;
			modal.style.display = 'none';
		}

		window.onclick = function(event) {
			if (event.target == modal) {
				// window.location.href = document.referrer;
				modal.style.display = 'none';
			}
		}

		document.getElementById("signup-form").onsubmit = function(e) {
			e.preventDefault();

			// Signup logic to send data to server/database
			window.location.href = document.referrer;
		}
	}
});
