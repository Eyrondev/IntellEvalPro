/**
 * Initialize navigation components
 * This script loads the navigation sidebar and header into any page
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 Admin navigation initializing...');
  
  // Load navigation components
  loadComponent('admin-sidebar', '/admin/navigation');
  loadComponent('admin-header', '/admin/header');
  
  // Track loaded components
  let loadedComponents = new Set();
  
  // Listen for component loaded events
  document.addEventListener('componentLoaded', function(e) {
    console.log('📢 Component loaded event:', e.detail.id);
    loadedComponents.add(e.detail.id);
    
    // Set active page when both components are loaded
    if (loadedComponents.has('admin-sidebar') && loadedComponents.has('admin-header')) {
      console.log('🎯 Both components loaded, setting active page');
      setTimeout(() => setActivePage(), 100);
    }
  });
  
  // Initialize mobile menu toggle
  setTimeout(function() {
    initializeAdminMobileMenu();
    
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
    
    // Backup: Set active page if components didn't load properly
    if (!loadedComponents.has('admin-sidebar') || !loadedComponents.has('admin-header')) {
      console.log('⚠️ Components may not have loaded, trying backup setActivePage');
      setActivePage();
    }
    
    // Hide loader
    const loader = document.getElementById('loader-overlay');
    if (loader) {
      loader.classList.add('opacity-0');
      setTimeout(() => {
        loader.style.display = 'none';
      }, 300);
    }
  }, 500); // Further increased delay for AWS
});

/**
 * Load HTML component into a container
 * @param {string} containerId - ID of the container element
 * @param {string} componentUrl - URL of the component to load
 */
function loadComponent(containerId, componentUrl) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`❌ Container not found: ${containerId}`);
    return;
  }
  
  console.log(`📦 Loading component: ${componentUrl} into ${containerId}`);
  
  fetch(componentUrl, {
    method: 'GET',
    credentials: 'same-origin', // Important for AWS to include session cookies
    headers: {
      'Accept': 'text/html',
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(response => {
      console.log(`📥 Response status for ${componentUrl}:`, response.status);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text();
    })
    .then(html => {
      console.log(`✅ Component loaded successfully: ${containerId}`);
      container.innerHTML = html;
      
      // Dispatch event when component is loaded
      const event = new CustomEvent('componentLoaded', { detail: { id: containerId } });
      document.dispatchEvent(event);
      
      // If this is the navigation component, set active page immediately
      if (containerId === 'admin-sidebar') {
        setTimeout(() => setActivePage(), 100);
      }
    })
    .catch(error => {
      console.error(`❌ Error loading component ${componentUrl}:`, error);
      container.innerHTML = `
        <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-600 text-sm">Failed to load component</p>
          <p class="text-red-500 text-xs mt-1">${error.message}</p>
          <button onclick="location.reload()" class="mt-2 text-xs text-red-700 underline">Reload Page</button>
        </div>
      `;
    });
}

/**
 * Initialize mobile menu functionality for admin
 */
function initializeAdminMobileMenu() {
  console.log('Initializing admin mobile menu...');
  
  // Wait to ensure elements are in DOM
  setTimeout(function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    console.log('Menu toggle element:', menuToggle);
    console.log('Sidebar element:', sidebar);
    
    if (!menuToggle) {
      console.error('Menu toggle button not found - ID: menu-toggle');
      return;
    }
    
    if (!sidebar) {
      console.error('Sidebar not found - ID: sidebar');
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
    
    console.log('✅ Admin mobile menu initialized successfully');
  }, 200); // Delay to ensure DOM is ready
}

/**
 * Set the active page in navigation based on current URL
 */
function setActivePage() {
  // Get current page path
  const currentPath = window.location.pathname;
  console.log('🔍 Setting active page for path:', currentPath);
  
  // Page mapping for breadcrumb updates (exact path matching)
  const pageMap = {
    '/admin/dashboard': 'Dashboard',
    '/admin/admin-dashboard': 'Dashboard',
    '/admin/user-management': 'User Management',
    '/admin/faculty-list': 'Faculty Management', 
    '/admin/student-list': 'Student Management',
    '/admin/subjects': 'Subjects Management',
    '/admin/sections': 'Section Management',
    '/admin/classes': 'Classes Management',
    '/admin/academic-years': 'Academic Years',
    '/admin/evaluation-periods': 'Evaluation Periods',
    '/admin/activity-logs': 'Activity Logs',
    '/admin/archives': 'Archives'
  };
  
  // Update breadcrumb - wait for element to exist
  let attempts = 0;
  const maxAttempts = 10;
  
  function updateBreadcrumb() {
    const currentPageElement = document.getElementById('current-page');
    if (currentPageElement) {
      const pageTitle = pageMap[currentPath] || 'Dashboard';
      currentPageElement.textContent = pageTitle;
      console.log('📝 Updated breadcrumb to:', pageTitle);
      
      // Keep original styling (no blue color)
      currentPageElement.classList.remove('text-primary-600');
      currentPageElement.classList.add('text-gray-500', 'font-medium');
      return true;
    } else {
      attempts++;
      if (attempts < maxAttempts) {
        console.log(`⏳ Breadcrumb element not found, retrying... (${attempts}/${maxAttempts})`);
        setTimeout(updateBreadcrumb, 100);
      } else {
        console.warn('⚠️ Breadcrumb element #current-page not found after', maxAttempts, 'attempts');
      }
      return false;
    }
  }
  
  updateBreadcrumb();
  
  // Set active class in navigation links
  let activeSet = false;
  const navLinks = document.querySelectorAll('.nav-link');
  console.log(`🔗 Found ${navLinks.length} navigation links`);
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    
    // Remove active classes first
    link.classList.remove('active', 'bg-gray-100', 'text-primary-700');
    
    if (href) {
      // Normalize paths for comparison
      const normalizedHref = href.replace(/\/$/, ''); // Remove trailing slash
      const normalizedPath = currentPath.replace(/\/$/, '');
      
      // Check for exact match first
      if (normalizedHref === normalizedPath) {
        link.classList.add('active', 'bg-gray-100', 'text-primary-700');
        activeSet = true;
        console.log('✅ Set active link (exact match):', href);
      }
      // Then check for partial match (for nested routes)
      else if (!activeSet && normalizedPath.startsWith(normalizedHref) && normalizedHref.length > 6) {
        link.classList.add('active', 'bg-gray-100', 'text-primary-700');
        activeSet = true;
        console.log('✅ Set active link (partial match):', href);
      }
    }
  });
  
  if (!activeSet) {
    console.warn('⚠️ No navigation link was set as active for path:', currentPath);
  }
}
