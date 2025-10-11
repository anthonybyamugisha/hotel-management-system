// Simple JavaScript for the hotel management system

document.addEventListener('DOMContentLoaded', function() {
    // Add click event to all buttons with class 'btn'
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Add loading effect
            this.classList.add('loading');
            this.innerHTML = 'Loading...';
            
            // Remove loading effect after 1 second
            setTimeout(() => {
                this.classList.remove('loading');
                this.innerHTML = this.dataset.originalText || this.innerHTML;
            }, 1000);
        });
    });
    
    // Add confirmation for report generation
    const reportLinks = document.querySelectorAll('a[href*="report"]');
    reportLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Store original text
            const button = this.closest('.report-card').querySelector('.btn');
            if (button) {
                button.dataset.originalText = button.innerHTML;
            }
        });
    });
    
    console.log('Hotel Management System JavaScript loaded');
});