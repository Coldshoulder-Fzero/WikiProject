// static/scripts.js
document.addEventListener("DOMContentLoaded", function () {
    const editButton = document.querySelector(".edit-page");
    const editModal = document.getElementById("edit-modal");
    const editForm = document.getElementById("edit-form");
    const closeModal = document.getElementById("close-modal");
    const contentArea = document.getElementById("content");

    if (editButton) {
        editButton.addEventListener("click", function () {
            const pageContent = document.querySelector(".page-content").textContent;
            contentArea.value = pageContent;
            editModal.style.display = "block";
        });
    }

    if (closeModal) {
        closeModal.addEventListener("click", function () {
            editModal.style.display = "none";
        });
    }

    if (editForm) {
        editForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const confirmChanges = confirm("Are you sure you want to save changes?");
            if (confirmChanges) {
                editForm.submit();
            }
        });
    }
});
