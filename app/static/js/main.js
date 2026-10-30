/**
 * BlogSphere - Main Client-Side JavaScript (Week 1)
 * Handles UI interactions, alert dismissal, and category pill filtering
 */

document.addEventListener('DOMContentLoaded', function () {
  console.log('BlogSphere platform initialized.');

  // 1. Auto-dismiss Bootstrap flash alerts after 5 seconds
  const flashAlerts = document.querySelectorAll('.alert-dismissible');
  flashAlerts.forEach(function (alert) {
    setTimeout(function () {
      alert.classList.remove('show');
      setTimeout(function () {
        alert.remove();
      }, 300);
    }, 5000);
  });

  // 2. Active navbar link highlighting based on current path
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link-custom');
  navLinks.forEach(function (link) {
    const linkPath = link.getAttribute('href');
    if (linkPath === currentPath) {
      link.classList.add('active');
    }
  });

  // 3. Category Pill filtering on homepage
  const categoryPills = document.querySelectorAll('.category-pill');
  const blogCards = document.querySelectorAll('.blog-card-item');

  if (categoryPills.length > 0 && blogCards.length > 0) {
    categoryPills.forEach(function (pill) {
      pill.addEventListener('click', function (e) {
        e.preventDefault();

        // Update active class
        categoryPills.forEach(p => p.classList.remove('active'));
        this.classList.add('active');

        const selectedCategory = this.getAttribute('data-category');

        blogCards.forEach(function (card) {
          const cardCategory = card.getAttribute('data-category');
          if (selectedCategory === 'All' || cardCategory === selectedCategory) {
            card.style.display = 'block';
            card.classList.add('animate-fade-in');
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 4. Contact form submission client-side enhancement
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function () {
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Sending Message...';
      }
    });
  }
});
