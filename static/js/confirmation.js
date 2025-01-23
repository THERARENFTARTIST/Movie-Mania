document.addEventListener('DOMContentLoaded', () => {
    // Highlight navbar links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.color = '#f39c12';
        });
        link.addEventListener('mouseout', () => {
            link.style.color = '#fff';
        });
    });

    // Add animation to the confirmation title
    const title = document.querySelector('.confirmation-title');
    title.style.transition = 'opacity 1s ease-in-out, transform 1s ease-in-out';
    title.style.opacity = '1';
    title.style.transform = 'translateY(0)';

    // Animate booking details on load
    const bookingDetails = document.querySelector('.booking-details');
    bookingDetails.style.transition = 'opacity 1.5s ease, transform 1.5s ease';
    bookingDetails.style.opacity = '1';
    bookingDetails.style.transform = 'translateY(0)';
});
