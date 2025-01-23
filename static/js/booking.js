document.addEventListener("DOMContentLoaded", function () {
    const bookingForm = document.getElementById("booking-form");

    bookingForm.addEventListener("submit", function (event) {
        // Validate inputs before submission
        const dateInput = document.getElementById("date").value;
        const timeInput = document.getElementById("time").value;
        const ticketsInput = document.getElementById("tickets").value;

        if (!dateInput || !timeInput || !ticketsInput) {
            event.preventDefault();
            alert("Please fill in all the required fields.");
            return;
        }

        if (ticketsInput < 1 || ticketsInput > 10) {
            event.preventDefault();
            alert("Number of tickets must be between 1 and 10.");
        }
    });
});
