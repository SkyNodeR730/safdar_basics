/**
 * Derma Shine Landing Page — Complete JavaScript
 * ES6 module-style IIFE. No external dependencies.
 */
(function () {
  'use strict';

  /* ================================================================
     UTILITIES
     ================================================================ */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  function getCsrf() {
    const meta = document.querySelector('meta[name="csrf-token"]')?.content || '';
    if (meta && meta !== 'None' && meta !== 'undefined') return meta;
    // Fallback: read from cookie (Frappe sets csrf_token cookie for some setups)
    const match = document.cookie.match(/(?:^|;)\s*csrf_token=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  async function ensureCsrf() {
    const token = getCsrf();
    if (token) return token;
    // Fetch a session token from Frappe before sending any POST
    try {
      const res = await fetch('/api/method/frappe.auth.get_logged_user', {
        credentials: 'same-origin',
      });
      // After this GET, Frappe sets the csrf_token cookie
      const match = document.cookie.match(/(?:^|;)\s*csrf_token=([^;]+)/);
      return match ? decodeURIComponent(match[1]) : '';
    } catch {
      return '';
    }
  }

  /* ================================================================
     NAVBAR — scroll glass effect + hamburger
     ================================================================ */
  function initNavbar() {
    const navbar = $('#mainNavbar');
    const hamburger = $('#hamburgerBtn');
    const mobileMenu = $('#mobileMenu');

    if (!navbar) return;

    // Scroll effect
    const onScroll = () => {
      navbar.classList.toggle('is-scrolled', window.scrollY > 30);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Hamburger toggle
    if (hamburger && mobileMenu) {
      hamburger.addEventListener('click', () => {
        const open = hamburger.classList.toggle('is-open');
        mobileMenu.classList.toggle('is-open', open);
        hamburger.setAttribute('aria-expanded', String(open));
        mobileMenu.setAttribute('aria-hidden', String(!open));
        document.body.style.overflow = open ? 'hidden' : '';
      });

      // Close on link click
      $$('.ds-mobile-menu__link', mobileMenu).forEach(link => {
        link.addEventListener('click', () => {
          hamburger.classList.remove('is-open');
          mobileMenu.classList.remove('is-open');
          hamburger.setAttribute('aria-expanded', 'false');
          mobileMenu.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        });
      });

      // Close on outside click
      document.addEventListener('click', (e) => {
        if (!navbar.contains(e.target) && mobileMenu.classList.contains('is-open')) {
          hamburger.classList.remove('is-open');
          mobileMenu.classList.remove('is-open');
          hamburger.setAttribute('aria-expanded', 'false');
          mobileMenu.setAttribute('aria-hidden', 'true');
          document.body.style.overflow = '';
        }
      });
    }
  }

  /* ================================================================
     SMOOTH SCROLL — offset for fixed navbar
     ================================================================ */
  function initSmoothScroll() {
    const navbarH = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue('--ds-navbar-h') || '72',
      10
    );

    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[href^="#"]');
      if (!link) return;

      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (!target) return;

      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - navbarH - 8;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  }

  /* ================================================================
     SCROLL REVEAL — Intersection Observer
     ================================================================ */
  function initScrollReveal() {
    const cards = $$('.ds-reveal');
    if (!cards.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const delay = parseInt(el.dataset.delay || '0', 10);
          setTimeout(() => el.classList.add('is-visible'), delay);
          observer.unobserve(el);
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );

    cards.forEach(card => observer.observe(card));
  }

  /* ================================================================
     PRODUCT LIGHTBOX
     ================================================================ */
  function initLightbox() {
    const lightbox   = $('#lightbox');
    const overlay    = $('#lightboxOverlay');
    const img        = $('#lightboxImg');
    const caption    = $('#lightboxCaption');
    const closeBtn   = $('#lightboxClose');
    const prevBtn    = $('#lightboxPrev');
    const nextBtn    = $('#lightboxNext');

    if (!lightbox) return;

    // Collect all lightbox-able products
    const items = $$('.ds-product-card__lightbox-btn');
    let currentIndex = 0;

    function openLightbox(index) {
      currentIndex = ((index % items.length) + items.length) % items.length;
      const btn = items[currentIndex];
      img.src = btn.dataset.src;
      img.alt = btn.dataset.alt;
      caption.textContent = btn.dataset.alt;
      lightbox.classList.add('is-open');
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      closeBtn.focus();
    }

    function closeLightbox() {
      lightbox.classList.remove('is-open');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      img.src = '';
    }

    function navigate(dir) {
      openLightbox(currentIndex + dir);
    }

    // Open buttons
    items.forEach((btn, i) => {
      btn.addEventListener('click', () => openLightbox(i));
    });

    // Controls
    closeBtn.addEventListener('click', closeLightbox);
    overlay.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', () => navigate(-1));
    nextBtn.addEventListener('click', () => navigate(1));

    // Keyboard
    lightbox.addEventListener('keydown', (e) => {
      if (e.key === 'Escape')      closeLightbox();
      if (e.key === 'ArrowLeft')   navigate(-1);
      if (e.key === 'ArrowRight')  navigate(1);
    });

    // Touch swipe
    let touchStartX = 0;
    lightbox.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
    lightbox.addEventListener('touchend', (e) => {
      const delta = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 50) navigate(delta < 0 ? 1 : -1);
    }, { passive: true });
  }

  /* ================================================================
     LOGIN MODAL
     ================================================================ */
  function initLoginModal() {
    const modal      = $('#loginModal');
    const overlay    = $('#loginOverlay');
    const closeBtn   = $('#loginClose');
    const form       = $('#loginForm');
    const userInput  = $('#loginUser');
    const passInput  = $('#loginPass');
    const togglePass = $('#togglePass');
    const eyeIcon    = $('#passEyeIcon');
    const submitBtn  = $('#loginSubmit');
    const btnText    = $('#loginBtnText');
    const spinner    = $('#loginSpinner');
    const rememberMe = $('#rememberMe');
    const userError  = $('#userError');
    const passError  = $('#passError');

    if (!modal) return;

    // Open triggers
    const openTriggers = ['#navLoginBtn', '#heroLoginBtn', '#mobileLoginBtn', '#ctaLoginBtn'];
    openTriggers.forEach(sel => {
      const btn = $(sel);
      if (btn) btn.addEventListener('click', openModal);
    });

    function openModal() {
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      setTimeout(() => userInput?.focus(), 100);

      // Restore remembered username
      const remembered = localStorage.getItem('ds_remember_user');
      if (remembered && userInput) {
        userInput.value = remembered;
        if (rememberMe) rememberMe.checked = true;
      }
    }

    function closeModal() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      clearErrors();
    }

    function clearErrors() {
      $$('.ds-field', modal).forEach(f => f.classList.remove('has-error'));
      if (userError) userError.textContent = '';
      if (passError) passError.textContent = '';
    }

    function setFieldError(field, errorEl, msg) {
      field.parentElement.parentElement.classList.add('has-error');
      errorEl.textContent = msg;
      field.focus();
    }

    function setLoading(loading) {
      submitBtn.disabled = loading;
      if (btnText) btnText.hidden = loading;
      if (spinner) spinner.hidden = !loading;
    }

    function validate() {
      clearErrors();
      let valid = true;

      const usr = userInput?.value.trim();
      const pwd = passInput?.value;

      if (!usr) {
        setFieldError(userInput, userError, 'Please enter your email or username.');
        valid = false;
      }

      if (!pwd) {
        if (valid) setFieldError(passInput, passError, 'Please enter your password.');
        else {
          passInput.parentElement.parentElement.classList.add('has-error');
          passError.textContent = 'Please enter your password.';
        }
        valid = false;
      } else if (pwd.length < 4) {
        if (valid) setFieldError(passInput, passError, 'Password seems too short.');
        valid = false;
      }

      return valid;
    }

    // Submit
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!validate()) return;

        setLoading(true);

        const usr = userInput.value.trim();
        const pwd = passInput.value;

        try {
          const csrf = await ensureCsrf();
          const response = await fetch('/api/method/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-Frappe-CSRF-Token': csrf,
              'Accept': 'application/json',
            },
            body: new URLSearchParams({ usr, pwd }),
            credentials: 'same-origin',
          });

          const data = await response.json();

          if (response.ok && data.message) {
            // Remember me
            if (rememberMe?.checked) {
              localStorage.setItem('ds_remember_user', usr);
            } else {
              localStorage.removeItem('ds_remember_user');
            }

            showToast('success', 'Login Successful', 'Welcome back! Redirecting to dashboard…');
            closeModal();
            setTimeout(() => { window.location.href = '/app'; }, 1200);
          } else {
            const msg = data.exc_type === 'AuthenticationError'
              ? 'Invalid credentials. Please check your username and password.'
              : data.message || 'Login failed. Please try again.';

            setFieldError(userInput, userError, msg);
            showToast('error', 'Login Failed', msg);
          }
        } catch (err) {
          const msg = 'Network error. Please check your connection.';
          showToast('error', 'Connection Error', msg);
          setFieldError(userInput, userError, msg);
        } finally {
          setLoading(false);
        }
      });
    }

    // Password toggle
    if (togglePass) {
      togglePass.addEventListener('click', () => {
        const isPass = passInput.type === 'password';
        passInput.type = isPass ? 'text' : 'password';
        eyeIcon.className = isPass ? 'fas fa-eye-slash' : 'fas fa-eye';
        togglePass.setAttribute('aria-label', isPass ? 'Hide password' : 'Show password');
      });
    }

    // Close
    closeBtn?.addEventListener('click', closeModal);
    overlay?.addEventListener('click', closeModal);

    // Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) closeModal();
    });

    // Focus trap
    modal.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab') return;
      const focusable = $$('button:not([disabled]), input, a[href]', modal);
      const first = focusable[0];
      const last  = focusable[focusable.length - 1];
      if (e.shiftKey ? document.activeElement === first : document.activeElement === last) {
        e.preventDefault();
        (e.shiftKey ? last : first).focus();
      }
    });
  }

  /* ================================================================
     TOAST NOTIFICATIONS
     ================================================================ */
  function showToast(type, title, message, duration = 5000) {
    const container = $('#toastContainer');
    if (!container) return;

    const icons = {
      success: 'fa-circle-check',
      error:   'fa-circle-xmark',
      info:    'fa-circle-info',
    };

    const toast = document.createElement('div');
    toast.className = `ds-toast ds-toast--${type}`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
      <i class="fas ${icons[type] || icons.info} ds-toast__icon" aria-hidden="true"></i>
      <div class="ds-toast__text">
        <div class="ds-toast__title">${escHtml(title)}</div>
        ${message ? `<div class="ds-toast__msg">${escHtml(message)}</div>` : ''}
      </div>
      <button class="ds-toast__close" aria-label="Dismiss notification">
        <i class="fas fa-xmark" aria-hidden="true"></i>
      </button>
    `;

    container.appendChild(toast);

    const dismiss = () => {
      toast.classList.add('is-exiting');
      toast.addEventListener('animationend', () => toast.remove(), { once: true });
    };

    toast.querySelector('.ds-toast__close').addEventListener('click', dismiss);
    const timer = setTimeout(dismiss, duration);
    toast.addEventListener('mouseenter', () => clearTimeout(timer));
  }

  /* ================================================================
     LOGOUT
     ================================================================ */
  function initLogout() {
    const btns = [$('#logoutBtn'), $('#heroLogoutBtn')].filter(Boolean);
    if (!btns.length) return;

    async function doLogout(el) {
      el.disabled = true;
      el.innerHTML = '<span class="ds-spinner" style="border-top-color:#fca5a5"></span>';
      try {
        const csrf = await ensureCsrf();
        await fetch('/api/method/logout', {
          method: 'POST',
          headers: { 'X-Frappe-CSRF-Token': csrf },
          credentials: 'same-origin',
        });
        showToast('info', 'Logged out', 'You have been signed out successfully.');
        setTimeout(() => { window.location.href = '/'; }, 1000);
      } catch {
        showToast('error', 'Error', 'Could not log out. Please try again.');
        el.disabled = false;
      }
    }

    btns.forEach(btn => btn.addEventListener('click', () => doLogout(btn)));
  }

  /* ================================================================
     NEWSLETTER
     ================================================================ */
  function initNewsletter() {
    const btn = $('#newsletterBtn');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const input = btn.previousElementSibling;
      const email = input?.value.trim();

      if (!email || !email.includes('@')) {
        showToast('error', 'Invalid Email', 'Please enter a valid email address.');
        input?.focus();
        return;
      }

      showToast('success', 'Subscribed!', 'You\'ll receive our latest updates soon.');
      if (input) input.value = '';
    });
  }

  /* ================================================================
     HERO PRODUCT CARDS — stagger animation
     ================================================================ */
  function initHeroCards() {
    $$('.ds-hero__product-card').forEach((card, i) => {
      card.style.animationDelay = `${0.4 + i * 0.08}s`;
    });
  }

  /* ================================================================
     ACTIVE NAV LINK — highlight current section
     ================================================================ */
  function initActiveNav() {
    const sections  = $$('section[id], div[id]');
    const navLinks  = $$('.ds-navbar__link');
    const navbarH   = 80;

    const onScroll = () => {
      const scrollY = window.scrollY + navbarH + 40;
      let current = '';

      sections.forEach(sec => {
        if (sec.offsetTop <= scrollY) current = sec.id;
      });

      navLinks.forEach(link => {
        const href = link.getAttribute('href');
        link.style.color = href === `#${current}`
          ? 'var(--ds-white)'
          : '';
        link.style.background = href === `#${current}`
          ? 'rgba(255, 255, 255, 0.1)'
          : '';
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ================================================================
     LAZY IMAGE LOADING (native + polyfill)
     ================================================================ */
  function initLazyLoad() {
    if ('loading' in HTMLImageElement.prototype) return;

    const imgs = $$('img[loading="lazy"]');
    if (!imgs.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          delete img.dataset.src;
        }
        observer.unobserve(img);
      });
    });

    imgs.forEach(img => observer.observe(img));
  }

  /* ================================================================
     HELPER — escape HTML
     ================================================================ */
  function escHtml(str) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#x27;' };
    return String(str).replace(/[&<>"']/g, c => map[c]);
  }

  /* ================================================================
     INIT
     ================================================================ */
  function init() {
    initNavbar();
    initSmoothScroll();
    initScrollReveal();
    initLightbox();
    initLoginModal();
    initLogout();
    initNewsletter();
    initHeroCards();
    initActiveNav();
    initLazyLoad();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
