async function loadNavbar() {
    try {
        const response = await fetch('./navbar.html');
        const html = await response.text();
        document.getElementById('navbar-container').innerHTML = html;
        
        // Initialize navbar event listeners after DOM is ready
        initNavbarEvents();
    } catch (error) {
        console.error('Error loading navbar:', error);
    }
}

function initNavbarEvents() {
    // Hamburger menu toggle for mobile
    const hamburger = document.getElementById('hamburger-toggle');
    const navItems = document.getElementById('nav-items');

    if (hamburger && navItems) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('open');
            navItems.classList.toggle('open');
        });

        // Close menu when clicking a nav link
        const navLinks = navItems.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('open');
                navItems.classList.remove('open');
            });
        });
    }

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
