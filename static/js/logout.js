document.getElementById('logout-btn').addEventListener('click', function (e) {
    e.preventDefault(); // Prevent default link behavior

    fetch('/logout', {
        method: 'GET',
        credentials: 'include', // Include session cookies
    })
        .then(response => {
            if (response.ok) {
                // Redirect to the home page
                window.location.href = '/index.html';
            } else {
                alert('Logout failed. Please try again.');
            }
        })
        .catch(error => console.error('Error during logout:', error));
});
