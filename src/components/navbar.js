async function loadNavbar() {
    try {
        const response = await fetch('../src/components/navbar.html');
        if (!response.ok) throw new Error('Failed to load navbar');
        const html = await response.text();
        
        // Insert at the beginning of body
        const body = document.body;
        body.insertAdjacentHTML('afterbegin', html);
        
        // Initialize navbar event listeners
        initNavbarEvents();
    } catch (error) {
        console.error('Error loading navbar:', error);
    }
}

function initNavbarEvents() {
    // Navbar dropdown toggle - click to toggle, hover to show
    const freeToolsDropdown = document.querySelector('#free-tools-toggle')?.parentElement;
    const servicesDropdown = document.querySelector('#services-toggle')?.parentElement;

    if (!freeToolsDropdown || !servicesDropdown) return;

    document.getElementById('free-tools-toggle')?.addEventListener('click', (e) => {
        const menu = document.getElementById('free-tools-menu');
        const toggle = e.currentTarget;
        menu?.classList.toggle('open');
        toggle?.classList.toggle('open');
    });

    document.getElementById('services-toggle')?.addEventListener('click', (e) => {
        const menu = document.getElementById('services-menu');
        const toggle = e.currentTarget;
        menu?.classList.toggle('open');
        toggle?.classList.toggle('open');
    });

    // Add hover support for dropdowns
    freeToolsDropdown.addEventListener('mouseenter', () => {
        document.getElementById('free-tools-menu')?.classList.add('open');
        document.getElementById('free-tools-toggle')?.classList.add('open');
    });

    freeToolsDropdown.addEventListener('mouseleave', () => {
        document.getElementById('free-tools-menu')?.classList.remove('open');
        document.getElementById('free-tools-toggle')?.classList.remove('open');
    });

    servicesDropdown.addEventListener('mouseenter', () => {
        document.getElementById('services-menu')?.classList.add('open');
        document.getElementById('services-toggle')?.classList.add('open');
    });

    servicesDropdown.addEventListener('mouseleave', () => {
        document.getElementById('services-menu')?.classList.remove('open');
        document.getElementById('services-toggle')?.classList.remove('open');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        const dropdowns = document.querySelectorAll('.dropdown');
        let clickedInDropdown = false;
        
        dropdowns.forEach(dropdown => {
            if (dropdown.contains(e.target)) {
                clickedInDropdown = true;
            }
        });
        
        if (!clickedInDropdown) {
            document.getElementById('free-tools-menu')?.classList.remove('open');
            document.getElementById('free-tools-toggle')?.classList.remove('open');
            document.getElementById('services-menu')?.classList.remove('open');
            document.getElementById('services-toggle')?.classList.remove('open');
        }
    });
}

// Load navbar when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadNavbar);
} else {
    loadNavbar();
}
