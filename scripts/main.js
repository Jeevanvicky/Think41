// ===== SMOOTH SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.getBoundingClientRect().top + window.pageYOffset - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===== NAVBAR SCROLL EFFECT =====
function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    const scrolled = window.scrollY;
    
    if (scrolled > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

// ===== ACTIVE NAV LINK =====
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop <= 100) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + currentSection) {
            link.classList.add('active');
        }
    });
}

// ===== SCROLL ANIMATIONS =====
function handleScrollAnimations() {
    const cards = document.querySelectorAll('.glass-card, .product-card, .login-card');
    
    cards.forEach(card => {
        const cardTop = card.getBoundingClientRect().top;
        const cardVisible = 100;
        
        if (cardTop < window.innerHeight - cardVisible) {
            card.classList.add('fade-in');
        }
    });
}

// ===== OPTIMIZED SCROLL HANDLER =====
let ticking = false;
function handleScroll() {
    if (!ticking) {
        requestAnimationFrame(() => {
            handleNavbarScroll();
            updateActiveNavLink();
            handleScrollAnimations();
            ticking = false;
        });
        ticking = true;
    }
}

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', function() {
    // Initial calls
    updateActiveNavLink();
    handleScrollAnimations();
    
    // Add scroll listener
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    // Stagger animation for product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.1) + 's';
    });
    
    // Stagger animation for login cards
    const loginCards = document.querySelectorAll('.login-card');
    loginCards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.1) + 's';
    });
});

// ===== NAVBAR TOGGLE =====
document.addEventListener('click', function(e) {
    const navbar = document.querySelector('.navbar-collapse');
    const toggler = document.querySelector('.navbar-toggler');
    
    if (!navbar.contains(e.target) && !toggler.contains(e.target)) {
        if (navbar.classList.contains('show')) {
            navbar.classList.remove('show');
        }
    }
});

// ===== PERFORMANCE OPTIMIZATION =====
window.addEventListener('load', function() {
    // Remove any loading states
    document.body.classList.add('loaded');
});

// ===== INTERSECTION OBSERVER FOR BETTER PERFORMANCE =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe all animated elements
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.glass-card, .product-card, .login-card');
    animatedElements.forEach(el => observer.observe(el));
});