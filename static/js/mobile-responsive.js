/**
 * Mobile Responsive Enhancements Script
 * Automatically adds mobile responsiveness to all IntellEvalPro pages
 */

document.addEventListener('DOMContentLoaded', function() {
  // Add responsive CSS if not already included
  if (!document.querySelector('link[href*="mobile-responsive.css"]')) {
    const responsiveCSS = document.createElement('link');
    responsiveCSS.rel = 'stylesheet';
  responsiveCSS.href = '/static/css/mobile-responsive.css';
    document.head.appendChild(responsiveCSS);
  }
  
  // Add mobile viewport meta tag if not present
  if (!document.querySelector('meta[name="viewport"]')) {
    const viewport = document.createElement('meta');
    viewport.name = 'viewport';
    viewport.content = 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no';
    document.head.appendChild(viewport);
  }
  
  // Enhanced mobile menu functionality
  function initializeMobileMenu() {
    const menuToggle = document.getElementById('menu-toggle') || document.querySelector('.mobile-menu-btn');
    const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
    let overlay = document.getElementById('sidebar-overlay');
    
    // Create overlay if it doesn't exist
    if (sidebar && !overlay) {
      overlay = document.createElement('div');
      overlay.id = 'sidebar-overlay';
      overlay.className = 'mobile-overlay';
      document.body.appendChild(overlay);
    }
    
    if (menuToggle && sidebar) {
      menuToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const isMobile = window.innerWidth < 1024;
        
        if (isMobile) {
          sidebar.classList.toggle('sidebar-mobile');
          sidebar.classList.toggle('show');
          if (overlay) {
            overlay.classList.toggle('show');
          }
        } else {
          sidebar.classList.toggle('-translate-x-full');
        }
      });
    }
    
    // Close sidebar when clicking overlay
    if (overlay) {
      overlay.addEventListener('click', function() {
        if (sidebar) {
          sidebar.classList.remove('show');
          sidebar.classList.add('sidebar-mobile');
        }
        overlay.classList.remove('show');
      });
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
      const isMobile = window.innerWidth < 1024;
      
      if (!isMobile) {
        // Desktop: show sidebar, hide overlay
        if (sidebar) {
          sidebar.classList.remove('sidebar-mobile', 'show', '-translate-x-full');
        }
        if (overlay) {
          overlay.classList.remove('show');
        }
      } else {
        // Mobile: hide sidebar by default
        if (sidebar && !sidebar.classList.contains('show')) {
          sidebar.classList.add('sidebar-mobile');
          sidebar.classList.remove('show');
        }
      }
    });
    
    // Initial setup based on screen size
    const isMobile = window.innerWidth < 1024;
    if (isMobile && sidebar) {
      sidebar.classList.add('sidebar-mobile');
    }
  }
  
  // Enhanced touch interactions
  function initializeTouchInteractions() {
    // Add touch-friendly classes to interactive elements
    const interactiveElements = document.querySelectorAll('button, .btn, .nav-link, a, .dropdown-toggle');
    
    interactiveElements.forEach(element => {
      // Ensure minimum touch target size
      const computedStyle = window.getComputedStyle(element);
      const minHeight = parseInt(computedStyle.minHeight) || 0;
      const minWidth = parseInt(computedStyle.minWidth) || 0;
      
      if (minHeight < 44) {
        element.style.minHeight = '44px';
      }
      if (minWidth < 44) {
        element.style.minWidth = '44px';
      }
      
      // Add touch feedback
      element.addEventListener('touchstart', function() {
        this.style.opacity = '0.7';
      });
      
      element.addEventListener('touchend', function() {
        this.style.opacity = '';
      });
      
      element.addEventListener('touchcancel', function() {
        this.style.opacity = '';
      });
    });
  }
  
  // Responsive table handling
  function initializeResponsiveTables() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
      if (!table.closest('.table-responsive')) {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive overflow-x-auto';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
      }
    });
  }
  
  // Responsive image handling
  function initializeResponsiveImages() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
      if (!img.classList.contains('fixed-size')) {
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
      }
    });
  }
  
  // Form input enhancements for mobile
  function initializeMobileFormEnhancements() {
    const inputs = document.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      // Prevent zoom on focus for iOS
      if (window.innerWidth <= 768) {
        const currentFontSize = window.getComputedStyle(input).fontSize;
        const fontSize = parseInt(currentFontSize);
        
        if (fontSize < 16) {
          input.style.fontSize = '16px';
        }
      }
      
      // Add mobile-friendly styling
      input.addEventListener('focus', function() {
        this.classList.add('mobile-focus');
      });
      
      input.addEventListener('blur', function() {
        this.classList.remove('mobile-focus');
      });
    });
  }
  
  // Initialize all mobile enhancements
  setTimeout(function() {
    initializeMobileMenu();
    initializeTouchInteractions();
    initializeResponsiveTables();
    initializeResponsiveImages();
    initializeMobileFormEnhancements();
  }, 100);
  
  // Performance optimization: debounced resize handler
  let resizeTimeout;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
      initializeMobileFormEnhancements();
    }, 250);
  });
  
  // Add mobile-specific CSS classes to body
  function updateBodyClasses() {
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth < 1024;
    const isDesktop = window.innerWidth >= 1024;
    
    document.body.classList.toggle('mobile-device', isMobile);
    document.body.classList.toggle('tablet-device', isTablet);
    document.body.classList.toggle('desktop-device', isDesktop);
  }
  
  updateBodyClasses();
  window.addEventListener('resize', updateBodyClasses);
});

// Utility functions for mobile responsiveness
window.MobileUtils = {
  isMobile: () => window.innerWidth < 768,
  isTablet: () => window.innerWidth >= 768 && window.innerWidth < 1024,
  isDesktop: () => window.innerWidth >= 1024,
  
  // Show/hide mobile sidebar
  toggleSidebar: function() {
    const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar) {
      sidebar.classList.toggle('show');
      sidebar.classList.toggle('sidebar-mobile');
    }
    
    if (overlay) {
      overlay.classList.toggle('show');
    }
  },
  
  // Close mobile sidebar
  closeSidebar: function() {
    const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar) {
      sidebar.classList.remove('show');
      sidebar.classList.add('sidebar-mobile');
    }
    
    if (overlay) {
      overlay.classList.remove('show');
    }
  },
  
  // Smooth scroll to element (mobile-optimized)
  scrollToElement: function(element, offset = 0) {
    if (typeof element === 'string') {
      element = document.querySelector(element);
    }
    
    if (element) {
      const elementTop = element.offsetTop - offset;
      window.scrollTo({
        top: elementTop,
        behavior: 'smooth'
      });
    }
  }
};