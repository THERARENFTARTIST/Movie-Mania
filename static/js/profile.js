document.addEventListener('DOMContentLoaded', () => {
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const changePasswordBtn = document.getElementById('change-password-btn');

    // Redirect to Edit Profile page
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', () => {
            window.location.href = '/edit-profile';
        });
    }

    // Redirect to Change Password page
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', () => {
            window.location.href = '/change-password';
        });
    }
});
