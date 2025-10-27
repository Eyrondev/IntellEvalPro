/**
 * Initialize navigation components
 * This script loads the navigation sidebar and header into any page
 */
document.addEventListener('DOMContentLoaded', function() {
  // Load navigation components
  // Determine if we're in admin folder or root folder
  const isInAdminFolder = window.location.pathname.includes('/admin/');
  const navPath = isInAdminFolder ? '/admin/navigation' : '/admin/navigation';
  const headerPath = isInAdminFolder ? '/admin/header' : '/admin/header';
  
  loadComponent('admin-sidebar', navPath);
  loadComponent('admin-header', headerPath);
  
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
  console.log('Current path:', currentPath);
  
  // Page mapping for breadcrumb updates
  const pageMap = {
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
  
  // Find and update breadcrumb
  const currentPageElement = document.getElementById('current-page');
  if (currentPageElement) {
    // Check for exact path match first
    if (pageMap[currentPath]) {
      currentPageElement.textContent = pageMap[currentPath];
      console.log('Updated breadcrumb to:', pageMap[currentPath]);
    } else {
      // Fallback: Check for partial path matches
      for (const [path, title] of Object.entries(pageMap)) {
        if (currentPath.includes(path.split('/').pop())) {
          currentPageElement.textContent = title;
          console.log('Updated breadcrumb (partial match) to:', title);
          break;
        }
      }
    }
    
    // Apply active styling to breadcrumb
    currentPageElement.classList.remove('text-gray-500');
    currentPageElement.classList.add('text-primary-600', 'font-semibold');
  }
  
  // Set active class in navigation links
  let activeSet = false;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    
    // Remove active classes first
    link.classList.remove('active', 'bg-gray-100', 'text-primary-700');
    
    if (href) {
      // Check for exact match first
      if (href === currentPath) {
        link.classList.add('active', 'bg-gray-100', 'text-primary-700');
        activeSet = true;
        console.log('Set active link (exact):', href);
      }
      // Then check for partial match (for nested routes)
      else if (!activeSet && currentPath.startsWith(href) && href.length > 1) {
        link.classList.add('active', 'bg-gray-100', 'text-primary-700');
        activeSet = true;
        console.log('Set active link (partial):', href);
      }
    }
  });
}
