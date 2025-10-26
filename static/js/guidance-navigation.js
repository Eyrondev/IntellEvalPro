/**
 * Initialize guidance navigation components
 * This script loads the navigation sidebar and header into any page
 */

/**
 * Load guidance navigation and header components
 * @param {string} activePage - The current active page identifier
 */
function loadGuidanceNavigation(activePage = '') {
  window.guidanceNavigationLoaded = true; // Mark as explicitly loaded
  
  console.log('Loading guidance navigation for page:', activePage);
  
  // Load header and sidebar components immediately (DOM is already ready when called from jQuery)
  $('#header-container').load('/guidance/header', function(response, status, xhr) {
    if (status === 'error') {
      console.error('Failed to load header:', xhr.status, xhr.statusText);
    } else {
      console.log('Header loaded successfully');
      
      // Update breadcrumb after header is loaded
      if (activePage) {
        updateGuidanceBreadcrumb(activePage);
      }
    }
  });
  
  $('#sidebar-container').load('/guidance/navigation', function(response, status, xhr) {
    if (status === 'error') {
      console.error('Failed to load sidebar:', xhr.status, xhr.statusText);
    } else {
      console.log('Sidebar loaded successfully');
      
      // Set active navigation after sidebar is loaded
      if (activePage) {
        setActiveGuidancePage(activePage);
      }
      
      // Initialize mobile menu toggle with a small delay to ensure DOM is ready
      setTimeout(function() {
        initializeGuidanceMobileMenu();
      }, 100);
    }
  });
}

/**
 * Initialize mobile menu functionality for guidance
 */
function initializeGuidanceMobileMenu() {
  console.log('Initializing guidance mobile menu...');
  
  // Wait a bit more to ensure elements are in DOM
  setTimeout(function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    console.log('Menu toggle element:', menuToggle);
    console.log('Sidebar element:', sidebar);
    
    if (!menuToggle) {
      console.error('Menu toggle button not found - ID: menu-toggle');
      console.log('Available buttons:', document.querySelectorAll('button'));
      return;
    }
    
    if (!sidebar) {
      console.error('Sidebar not found - ID: sidebar');
      console.log('Available elements with sidebar:', document.querySelectorAll('[id*="sidebar"]'));
      return;
    }
    
    console.log('Menu toggle and sidebar found, setting up event listeners');
    console.log('Sidebar classes:', sidebar.className);
    
    // Create overlay if it doesn't exist
    let overlay = document.getElementById('sidebar-overlay');
    if (!overlay) {
      console.log('Creating overlay element...');
      overlay = document.createElement('div');
      overlay.id = 'sidebar-overlay';
      overlay.className = 'fixed inset-0 bg-gray-900 bg-opacity-50 z-30 lg:hidden hidden transition-opacity duration-300';
      document.body.appendChild(overlay);
      console.log('Overlay created');
    }
    
    // Remove any existing event listeners by cloning
    const newMenuToggle = menuToggle.cloneNode(true);
    menuToggle.parentNode.replaceChild(newMenuToggle, menuToggle);
    
    // Toggle sidebar on button click
    newMenuToggle.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      console.log('🍔 Menu toggle clicked!');
      console.log('Before toggle - Sidebar classes:', sidebar.className);
      
      const isHidden = sidebar.classList.contains('-translate-x-full');
      console.log('Is sidebar hidden?', isHidden);
      
      sidebar.classList.toggle('-translate-x-full');
      overlay.classList.toggle('hidden');
      
      console.log('After toggle - Sidebar classes:', sidebar.className);
      console.log('After toggle - Overlay classes:', overlay.className);
      
      // Prevent body scroll when menu is open
      if (!sidebar.classList.contains('-translate-x-full')) {
        document.body.style.overflow = 'hidden';
        console.log('Menu opened - body scroll disabled');
      } else {
        document.body.style.overflow = '';
        console.log('Menu closed - body scroll enabled');
      }
    });
    
    // Close sidebar when overlay is clicked
    overlay.addEventListener('click', function() {
      console.log('Overlay clicked, closing sidebar');
      sidebar.classList.add('-translate-x-full');
      overlay.classList.add('hidden');
      document.body.style.overflow = '';
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(event) {
      if (window.innerWidth < 1024) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnToggle = newMenuToggle.contains(event.target);
        const isSidebarOpen = !sidebar.classList.contains('-translate-x-full');
        
        if (!isClickInsideSidebar && !isClickOnToggle && isSidebarOpen) {
          console.log('Click outside detected, closing sidebar');
          sidebar.classList.add('-translate-x-full');
          overlay.classList.add('hidden');
          document.body.style.overflow = '';
        }
      }
    });
    
    // Close sidebar when window is resized to desktop
    window.addEventListener('resize', function() {
      if (window.innerWidth >= 1024) {
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
      }
    });
    
    console.log('✅ Mobile menu initialized successfully');
  }, 200); // Increased delay to ensure DOM is ready
}

/**
 * Set active page in guidance navigation
 */
function setActiveGuidancePage(activePage) {
  // Use setTimeout to ensure DOM is fully loaded
  setTimeout(function() {
    console.log('Setting active page:', activePage);
    
    // Remove active class from all navigation links
    $('.nav-link').removeClass('active-nav bg-orange-50 text-orange-600');
    
    // Set active based on page identifier
    const pageMap = {
      'guidance-dashboard': '/guidance/guidance-dashboard',
      'student-management': '/guidance/student-management',
      'faculty-management': '/guidance/faculty-management',
      'evaluation-periods': '/guidance/evaluation-periods',
      'evaluation-results': '/guidance/evaluation-results',
      'evaluation-monitoring': '/guidance/evaluation-monitoring',
      'questionnaire-management': '/guidance/questionnaire-management',
      'evaluation-reports': '/guidance/evaluation-reports',
      'faculty-performance': '/guidance/faculty-performance',
      'faculty-performance-analytics': '/analytics/faculty-performance',
      'response-analytics': '/analytics/response-analytics',
      'ai-analytics': '/guidance/ai-analytics',
      'rankings': '/analytics/rankings',
      'my-profile': '/guidance/my-profile',
      'settings': '/guidance/settings',
      'help-support': '/guidance/help-support'
    };
    
    if (pageMap[activePage]) {
      const targetHref = pageMap[activePage];
      console.log('Looking for link with href:', targetHref);
      
      const $link = $(`a[href="${targetHref}"]`);
      console.log('Found links:', $link.length);
      
      if ($link.length > 0) {
        $link.addClass('active-nav');
        console.log('✅ Active navigation set for:', activePage);
      } else {
        console.warn('❌ Navigation link not found for:', activePage, targetHref);
      }
    } else {
      console.warn('⚠️  Page not found in pageMap:', activePage);
    }
  }, 300); // Delay to ensure sidebar is fully rendered
}

/**
 * Update breadcrumb with current page title
 */
function updateGuidanceBreadcrumb(activePage) {
  // Map page identifiers to display titles
  const pageTitles = {
    'guidance-dashboard': 'Guidance Dashboard',
    'student-management': 'Student Management',
    'faculty-management': 'Faculty Management',
    'evaluation-periods': 'Evaluation Periods',
    'evaluation-results': 'Evaluation Results',
    'evaluation-monitoring': 'Evaluation Monitoring',
    'questionnaire-management': 'Questionnaire Management',
    'evaluation-reports': 'Evaluation Reports',
    'faculty-performance': 'Faculty Performance',
    'faculty-performance-analytics': 'Faculty Performance Analytics',
    'response-analytics': 'Response Analytics',
    'ai-analytics': 'AI Analytics Dashboard',
    'rankings': 'Rankings',
    'my-profile': 'My Profile',
    'settings': 'Settings',
    'help-support': 'Help & Support'
  };
  
  const pageTitle = pageTitles[activePage] || 'Guidance Dashboard';
  
  // Update breadcrumb after a short delay to ensure header is loaded
  setTimeout(function() {
    const currentPageElement = document.getElementById('current-page');
    if (currentPageElement) {
      currentPageElement.textContent = pageTitle;
      console.log('Breadcrumb updated to:', pageTitle);
    }
  }, 100);
}

// Legacy support - auto-initialize if no explicit call
document.addEventListener('DOMContentLoaded', function() {
  // Only auto-initialize if loadGuidanceNavigation hasn't been called
  if (!window.guidanceNavigationLoaded) {
    // Load navigation components
    const isInGuidanceFolder = window.location.pathname.includes('/guidance/');
    const navPath = isInGuidanceFolder ? '/guidance/navigation' : '/guidance/navigation';
    const headerPath = isInGuidanceFolder ? '/guidance/header' : '/guidance/header';
    
    loadComponent('guidance-sidebar', navPath);
    loadComponent('guidance-header', headerPath);
    
    // Initialize mobile menu toggle
    setTimeout(function() {
      const menuToggleButton = document.getElementById('menu-toggle');
      const sidebar = document.getElementById('sidebar');
      
      if (menuToggleButton && sidebar) {
        menuToggleButton.addEventListener('click', function() {
          sidebar.classList.toggle('-translate-x-full');
        });
      }
      
      // Initialize dropdown toggles
      document.querySelectorAll('.nav-link .fa-chevron-down').forEach(icon => {
        const button = icon.closest('button');
        if (button) {
          button.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            const chevron = this.querySelector('.fa-chevron-down');
            
            dropdown.classList.toggle('hidden');
            chevron.classList.toggle('rotate-180');
          });
        }
      });
      
      // Set active page in navigation
      setActivePage();
      
      // Hide loader
      const loader = document.getElementById('loader-overlay');
      if (loader) {
        loader.classList.add('opacity-0');
        setTimeout(() => {
          loader.style.display = 'none';
        }, 300);
      }
    }, 100);
  }
});

/**
 * Load HTML component into a container
 * @param {string} containerId - ID of the container element
 * @param {string} componentUrl - URL of the component to load
 */
function loadComponent(containerId, componentUrl) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  fetch(componentUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text();
    })
    .then(html => {
      container.innerHTML = html;
      
      // Dispatch event when component is loaded
      const event = new CustomEvent('componentLoaded', { detail: { id: containerId } });
      document.dispatchEvent(event);
    })
    .catch(error => {
      console.error('Error loading component:', error);
      container.innerHTML = `<p class="text-red-500 p-4">Failed to load component: ${error.message}</p>`;
    });
}

/**
 * Set the active page in navigation based on current URL
 */
function setActivePage() {
  // Get current page path
  const currentPath = window.location.pathname;
  
  // Find and update breadcrumb
  const currentPageElement = document.getElementById('current-page');
  if (currentPageElement) {
    if (currentPath.includes('student-management')) {
      currentPageElement.textContent = 'Student Management';
    } else if (currentPath.includes('academic-advising')) {
      currentPageElement.textContent = 'Academic Advising';
    } else if (currentPath.includes('career-counseling')) {
      currentPageElement.textContent = 'Career Counseling';
    } else if (currentPath.includes('student-records')) {
      currentPageElement.textContent = 'Student Records';
    } else if (currentPath.includes('appointments')) {
      currentPageElement.textContent = 'Appointments';
    }
    // Add more conditions for other pages as needed
  }
  
  // Set active class in navigation
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href.replace('/', ''))) {
      // Remove active class from all links
      document.querySelectorAll('.nav-link').forEach(el => {
        el.classList.remove('active-nav', 'active', 'bg-gray-100', 'text-primary-700');
      });
      
      // Add active class to current link
      link.classList.add('active-nav');
    }
  });
}
