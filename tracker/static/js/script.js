
// Auto-submit filter
document.querySelectorAll('select[name="month"], select[name="year"]').forEach(select => {
    select.addEventListener('change', function () {
        this.closest('form').submit();
    });
});

// Auto-hide messages
document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.alert-premium');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s';
            setTimeout(() => msg.remove(), 500);
        }, 3000);
    });

    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            this.parentElement.remove();
        });
    });
});