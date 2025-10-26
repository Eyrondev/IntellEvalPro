// Initialize the navigation system

document.addEventListener('DOMContentLoaded', function() {
  // Get the current page URL
  const currentPage = window.location.pathname;
  
  // Determine user role from the page or session
  // This is a simple implementation - in production, this would come from authentication
  let userRole = 'admin'; // Default role
  
  if (currentPage.includes('/student/')) {
    userRole = 'student';
  } else if (currentPage.includes('/guidance/')) {
    userRole = 'guidance';
  }
  
  // Update user role display in the UI
  const userRoleElement = document.getElementById('user-role');
  if (userRoleElement) {
    userRoleElement.textContent = userRole.charAt(0).toUpperCase() + userRole.slice(1);
  }
  
  // Get navigation menus based on role
  try {
    // If navigation.js is loaded, use it to initialize navigation
    if (typeof initializeNavigation === 'function') {
      initializeNavigation(userRole, currentPage);
    } else {
      console.error('Navigation module not loaded');
    }
  } catch (error) {
    console.error('Error initializing navigation:', error);
  }
  
  // Highlight the active navigation link
  highlightActiveNavLink();
});

/**
 * Highlights the active navigation link in the sidebar
 */
function highlightActiveNavLink() {
  const currentPath = window.location.pathname;
  
  // Find all navigation links
  const navLinks = document.querySelectorAll('.nav-link');
  
  // Remove active class from all links
  navLinks.forEach(link => {
    link.classList.remove('active', 'bg-gray-100', 'border-l-4', 'border-primary-500');
  });
  
  // Find the matching link and add active class
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href) {
      // Extract the path from the href
      const hrefPath = href.split('/').pop();
      const currentPathSegments = currentPath.split('/');
      const currentPathEnd = currentPathSegments[currentPathSegments.length - 1];
      
      // Check if this is the active link
      if (href === currentPath || hrefPath === currentPathEnd) {
        link.classList.add('active', 'bg-primary-50', 'border-l-4', 'border-primary-500');
      }
    }
  });
}

/**
 * Updates the page title and breadcrumbs based on current page
 * @param {string} pageTitle - The title of the current page
 * @param {Array} breadcrumbs - Array of breadcrumb objects with label and url
 */
function updatePageHeader(pageTitle, breadcrumbs) {
  // Update page title if element exists
  const currentPageElement = document.getElementById('current-page');
  if (currentPageElement && pageTitle) {
    currentPageElement.textContent = pageTitle;
    
    // Update document title as well
    document.title = pageTitle + ' - IntellEvalPro';
  }
  
  // Update breadcrumbs if provided
  if (breadcrumbs && Array.isArray(breadcrumbs)) {
    const breadcrumbsContainer = document.querySelector('[aria-label="Breadcrumb"] ol');
    if (breadcrumbsContainer) {
      // Always start with home
      let breadcrumbsHtml = `
        <li class="inline-flex items-center">
          <a href="/dashboard.html" class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-primary-600">
            <i class="fas fa-home w-4 h-4 mr-2"></i>
            Home
          </a>
        </li>
      `;
      
      // Add additional breadcrumbs
      breadcrumbs.forEach((crumb, index) => {
        const isLast = index === breadcrumbs.length - 1;
        breadcrumbsHtml += `
          <li>
            <div class="flex items-center">
              <i class="fas fa-chevron-right w-3 h-3 text-gray-400 mx-1"></i>
              ${isLast 
                ? `<span class="ml-1 text-sm font-medium text-gray-500">${crumb.label}</span>`
                : `<a href="${crumb.url}" class="ml-1 text-sm font-medium text-gray-700 hover:text-primary-600">${crumb.label}</a>`
              }
            </div>
          </li>
        `;
      });
      
      breadcrumbsContainer.innerHTML = breadcrumbsHtml;
    }
  }
}
