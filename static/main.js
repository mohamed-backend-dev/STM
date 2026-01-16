// Fade in effect
document.addEventListener("DOMContentLoaded", () => {
    document.body.style.opacity = "0";
    document.body.style.transition = "opacity 0.4s ease";
    setTimeout(() => {
        document.body.style.opacity = "1";
    }, 100);
});

// Confirm delete (يحمي المستخدم من الخطأ)
const deleteInput = document.querySelector('input[name="delete"]');

if (deleteInput) {
    deleteInput.form.addEventListener("submit", (e) => {
        if (deleteInput.value.trim() !== "") {
            const ok = confirm("Are you sure you want to delete this task?");
            if (!ok) {
                e.preventDefault();
            }
        }
    });
}
// last commit
// ops