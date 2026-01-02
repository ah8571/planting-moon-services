// Load footer component
async function loadFooter() {
    try {
        // Determine correct path based on current location
        const path = window.location.pathname;
        const footerPath = path.startsWith('/pages/') || path === '/pages' ? './footer.html' : './components/footer.html';
        const response = await fetch(footerPath);
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
