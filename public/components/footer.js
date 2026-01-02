// Load footer component
async function loadFooter() {
    try {
        const response = await fetch('./components/footer.html');
        const footerHTML = await response.text();
        document.getElementById('footer-container').innerHTML = footerHTML;
    } catch (error) {
        console.error('Error loading footer component:', error);
    }
}

// Load footer when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadFooter);
} else {
    loadFooter();
}
