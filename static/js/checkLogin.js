document.addEventListener("DOMContentLoaded", function () {
    const browseMoviesBtn = document.getElementById("browseMoviesBtn");

    browseMoviesBtn.addEventListener("click", function (event) {
        // Read login status from the data attribute
        const isLoggedIn = document.body.getAttribute("data-is-logged-in") === "true";

        if (!isLoggedIn) {
            event.preventDefault();
            alert("User login is required to browse movies.");
            window.location.href = '/login'; // Redirect to the login page
        }
    });
});
