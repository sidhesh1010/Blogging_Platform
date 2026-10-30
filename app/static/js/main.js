/**
 * BlogSphere - Main Client-Side JavaScript
 * Enhanced for Week 4: Responsive Frontend Polish & Medium-like Reading Interface
 */

document.addEventListener('DOMContentLoaded', function () {
  console.log('BlogSphere platform initialized with Week 4 interactive suite.');

  // =========================================================================
  // 1. Dark / Light Mode Switcher with LocalStorage Persistence
  // =========================================================================
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');

  function getPreferredTheme() {
    const stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);

    if (themeIcon) {
      if (theme === 'dark') {
        themeIcon.classList.remove('bi-moon-stars');
        themeIcon.classList.add('bi-sun');
        if (themeToggleBtn) themeToggleBtn.title = 'Switch to Light Theme';
      } else {
        themeIcon.classList.remove('bi-sun');
        themeIcon.classList.add('bi-moon-stars');
        if (themeToggleBtn) themeToggleBtn.title = 'Switch to Dark Theme';
      }
    }
  }

  // Initial theme application
  applyTheme(getPreferredTheme());

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-bs-theme') || 'light';
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
    });
  }

  // =========================================================================
  // 2. Reading Progress Bar for Article Reading (Medium-Style)
  // =========================================================================
  const progressBar = document.getElementById('readingProgressBar');
  const articleContent = document.querySelector('.article-body-content') || document.querySelector('article');

  if (progressBar && articleContent) {
    window.addEventListener('scroll', function () {
      const windowHeight = window.innerHeight;
      const docHeight = document.documentElement.scrollHeight;
      const scrollTop = window.scrollY;
      const maxScroll = docHeight - windowHeight;

      if (maxScroll > 0) {
        const progress = Math.min(100, Math.max(0, (scrollTop / maxScroll) * 100));
        progressBar.style.width = progress + '%';
      }
    }, { passive: true });
  }

  // =========================================================================
  // 3. Reader Mode Controls (Serif / Sans, Font Size, Column Width)
  // =========================================================================
  const readerFontFamilyBtn = document.getElementById('readerFontFamilyBtn');
  const readerFontSmBtn = document.getElementById('readerFontSmBtn');
  const readerFontMdBtn = document.getElementById('readerFontMdBtn');
  const readerFontLgBtn = document.getElementById('readerFontLgBtn');
  const readerWidthBtn = document.getElementById('readerWidthBtn');
  const readerContainer = document.getElementById('articleReaderContainer');

  if (articleContent) {
    // Restore reader settings
    const savedFont = localStorage.getItem('readerFont') || 'sans';
    const savedSize = localStorage.getItem('readerSize') || 'md';
    const savedWidth = localStorage.getItem('readerWidth') || 'standard';

    if (savedFont === 'serif') articleContent.classList.add('reader-serif');
    articleContent.classList.add('reader-font-' + savedSize);
    if (readerContainer && savedWidth === 'wide') readerContainer.classList.add('reader-width-wide');

    // Font Family Switcher
    if (readerFontFamilyBtn) {
      readerFontFamilyBtn.addEventListener('click', function () {
        articleContent.classList.toggle('reader-serif');
        const isSerif = articleContent.classList.contains('reader-serif');
        localStorage.setItem('readerFont', isSerif ? 'serif' : 'sans');
        readerFontFamilyBtn.innerHTML = isSerif 
          ? '<i class="bi bi-fonts me-1"></i> Sans-Serif' 
          : '<i class="bi bi-book me-1"></i> Editorial Serif';
      });
    }

    // Font Size Adjusters
    function setFontSize(size) {
      articleContent.classList.remove('reader-font-sm', 'reader-font-md', 'reader-font-lg');
      articleContent.classList.add('reader-font-' + size);
      localStorage.setItem('readerSize', size);
      [readerFontSmBtn, readerFontMdBtn, readerFontLgBtn].forEach(btn => btn && btn.classList.remove('active'));
      const activeBtn = size === 'sm' ? readerFontSmBtn : (size === 'lg' ? readerFontLgBtn : readerFontMdBtn);
      if (activeBtn) activeBtn.classList.add('active');
    }

    if (readerFontSmBtn) readerFontSmBtn.addEventListener('click', () => setFontSize('sm'));
    if (readerFontMdBtn) readerFontMdBtn.addEventListener('click', () => setFontSize('md'));
    if (readerFontLgBtn) readerFontLgBtn.addEventListener('click', () => setFontSize('lg'));

    // Reader Width Switcher
    if (readerWidthBtn && readerContainer) {
      readerWidthBtn.addEventListener('click', function () {
        readerContainer.classList.toggle('reader-width-wide');
        const isWide = readerContainer.classList.contains('reader-width-wide');
        localStorage.setItem('readerWidth', isWide ? 'wide' : 'standard');
        readerWidthBtn.classList.toggle('active', isWide);
      });
    }
  }

  // =========================================================================
  // 4. Code Blocks: One-Click Copy to Clipboard
  // =========================================================================
  const codeBlocks = document.querySelectorAll('.article-body-content pre');
  codeBlocks.forEach(function (pre) {
    // Avoid double buttons
    if (pre.querySelector('.code-copy-btn')) return;

    const copyBtn = document.createElement('button');
    copyBtn.className = 'code-copy-btn';
    copyBtn.type = 'button';
    copyBtn.innerHTML = '<i class="bi bi-clipboard"></i> Copy';

    copyBtn.addEventListener('click', function () {
      const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
      navigator.clipboard.writeText(code).then(() => {
        copyBtn.innerHTML = '<i class="bi bi-check2"></i> Copied!';
        copyBtn.classList.add('copied');
        setTimeout(() => {
          copyBtn.innerHTML = '<i class="bi bi-clipboard"></i> Copy';
          copyBtn.classList.remove('copied');
        }, 2000);
      }).catch(err => {
        console.error('Copy failed:', err);
      });
    });

    pre.appendChild(copyBtn);
  });

  // =========================================================================
  // 5. Floating Back-to-Top Button
  // =========================================================================
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (backToTopBtn) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 320) {
        backToTopBtn.classList.add('show');
      } else {
        backToTopBtn.classList.remove('show');
      }
    }, { passive: true });

    backToTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // =========================================================================
  // 6. Interactive Bookmark / Save Story Toggle (Client-side)
  // =========================================================================
  const bookmarkBtns = document.querySelectorAll('.btn-bookmark-story');
  let savedBookmarks = JSON.parse(localStorage.getItem('blogsphere_bookmarks') || '[]');

  bookmarkBtns.forEach(function (btn) {
    const postId = btn.getAttribute('data-post-id');
    const isBookmarked = savedBookmarks.includes(postId);

    if (isBookmarked) {
      btn.classList.add('active');
      const icon = btn.querySelector('i');
      if (icon) {
        icon.classList.remove('bi-bookmark');
        icon.classList.add('bi-bookmark-fill', 'text-primary');
      }
    }

    btn.addEventListener('click', function () {
      if (savedBookmarks.includes(postId)) {
        savedBookmarks = savedBookmarks.filter(id => id !== postId);
        btn.classList.remove('active');
        const icon = btn.querySelector('i');
        if (icon) {
          icon.classList.remove('bi-bookmark-fill', 'text-primary');
          icon.classList.add('bi-bookmark');
        }
      } else {
        savedBookmarks.push(postId);
        btn.classList.add('active');
        const icon = btn.querySelector('i');
        if (icon) {
          icon.classList.remove('bi-bookmark');
          icon.classList.add('bi-bookmark-fill', 'text-primary');
        }
      }
      localStorage.setItem('blogsphere_bookmarks', JSON.stringify(savedBookmarks));
    });
  });

  // =========================================================================
  // 7. Live Real-Time Search & Category Filtering on Homepage
  // =========================================================================
  const searchInput = document.getElementById('articleSearchInput');
  const categoryPills = document.querySelectorAll('.category-pill');
  const blogCards = document.querySelectorAll('.blog-card-item');
  const noResultsAlert = document.getElementById('noSearchResults');

  function filterArticles() {
    if (!blogCards.length) return;

    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const activePill = document.querySelector('.category-pill.active');
    const selectedCategory = activePill ? activePill.getAttribute('data-category') : 'All';

    let visibleCount = 0;

    blogCards.forEach(function (card) {
      const cardCategory = card.getAttribute('data-category') || '';
      const cardText = card.innerText.toLowerCase();

      const matchesCategory = selectedCategory === 'All' || cardCategory === selectedCategory;
      const matchesSearch = !query || cardText.includes(query);

      if (matchesCategory && matchesSearch) {
        card.style.display = '';
        card.classList.add('animate-fade-in');
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (noResultsAlert) {
      noResultsAlert.classList.toggle('d-none', visibleCount > 0);
    }
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterArticles);
  }

  if (categoryPills.length > 0) {
    categoryPills.forEach(function (pill) {
      pill.addEventListener('click', function (e) {
        e.preventDefault();
        categoryPills.forEach(p => p.classList.remove('active'));
        this.classList.add('active');
        filterArticles();
      });
    });
  }

  // =========================================================================
  // 8. Auto-dismiss Flash Alerts
  // =========================================================================
  const flashAlerts = document.querySelectorAll('.alert-dismissible');
  flashAlerts.forEach(function (alert) {
    setTimeout(function () {
      alert.classList.remove('show');
      setTimeout(function () {
        alert.remove();
      }, 300);
    }, 5000);
  });

  // =========================================================================
  // 9. Active Navbar Link Highlighting
  // =========================================================================
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link-custom');
  navLinks.forEach(function (link) {
    const linkPath = link.getAttribute('href');
    if (linkPath === currentPath) {
      link.classList.add('active');
    }
  });
});
