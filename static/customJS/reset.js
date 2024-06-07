(function () {
	'use strict'

	// Fetch all the forms we want to apply custom Bootstrap validation styles to
	var forms = document.querySelectorAll('.needs-validation')

	// Loop over them and prevent submission
	Array.prototype.slice.call(forms)
		.forEach(function (form) {
			form.addEventListener('submit', function (event) {
				event.preventDefault()
				event.stopPropagation()

				if (form.checkValidity()) {
					// Form is valid, proceed with fetch request
					let formData = new FormData(form);
					let data = {
						email: formData.get('email'),
						current_password: formData.get('current-password'),
						new_password: formData.get('new-password'),
						confirm_password: formData.get('confirm-password')
					};
                    console.log(data);

					fetch('/reset', {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(data)
					})
					.then(response => {
						if (!response.ok) {
							return response.json().then(err => { throw err; });
						}
						return response.json();
					})
					.then(data => {
						// Handle success - you might want to redirect to a success page or show a message
						window.location.href = "/reset/success";
					})
					.catch(error => {
						// Handle error - show a message to the user
						console.error('Error:', error);
						alert('There was an error with your request: ' + error.detail);
					});
				}

				form.classList.add('was-validated')
			}, false)
		})
})()