// Add an event listener to wait for the DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Get the references to the necessary HTML elements
    const editButton = document.querySelector(".edit-page"); // Edit button
    const editModal = document.getElementById("edit-modal"); // Edit modal dialog
    const editForm = document.getElementById("edit-form"); // Edit form inside the modal
    const closeModal = document.getElementById("close-modal"); // Close button for the modal
    const contentArea = document.getElementById("content"); // Content area in the edit form
    // Check if the editButton exists on the page
if (editButton) {
    // Add a click event listener to the editButton
    editButton.addEventListener("click", function () {
        // Get the text content of the ".page-content" element
        const pageContent = document.querySelector(".page-content").textContent;
        // Set the contentArea value to the text content of the ".page-content" element
        contentArea.value = pageContent;
        // Display the edit modal
        editModal.style.display = "block";
    });
}

// Check if the closeModal exists on the page
if (closeModal) {
    // Add a click event listener to the closeModal button
    closeModal.addEventListener("click", function () {
        // Hide the edit modal
        editModal.style.display = "none";
    });
}

// Check if the editForm exists on the page
if (editForm) {
    // Add a submit event listener to the editForm
    editForm.addEventListener("submit", function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Show a confirmation dialog before saving the changes
        const confirmChanges = confirm("Are you sure you want to save changes?");
        // Check if the user has confirmed the changes
        if (confirmChanges) {
            // Submit the edit form
            editForm.submit();
        }
    });
}
});

