/**
 * Unified Student Navigation Loader
 * Provides consistent navigation and header loading across all student pages
 */

// Configuration object for different pages
const PAGE_CONFIG = {
  'student-dashboard': {
    href: '/student/student-dashboard',
    title: 'Dashboard'
  },
  'pending-evaluations': {
    href: '/student/pending-evaluations', 
    title: 'Pending Evaluations'
  },
  'my-evaluations': {
    href: '/student/my-evaluations',
    title: 'My Evaluations'
  },
  'my-profile': {
    href: '/student/my-profile',
    title: 'My Profile'
  },
  'evaluation-form': {
    href: '/student/evaluation-form',
    title: 'Evaluation Form'
  },
  'help-support': {
    href: '/student/help-support',
    title: 'Help & Support'
  },
  'settings': {
    href: '/student/settings',
    title: 'Settings'
  }
};

/**
 * Load navigation and header components
 * @param {string} activePage - The key from PAGE_CONFIG for the current page
 */
function loadStudentNavigation(activePage = '') {
  // Load navigation and header components
  document.addEventListener('DOMContentLoaded', function() {
    $('#header-container').load('/student/header', function() {
      // Header loaded successfully, now update breadcrumb
      console.log('Header loaded, initializing...');
      
      // Update breadcrumb after header is loaded
      if (activePage) {
        updateStudentBreadcrumb(activePage);
      }
    });

    $('#sidebar-container').load('/student/navigation', function() {
      // Update active navigation
      $('.nav-link').removeClass('bg-primary-100 text-primary-700');
      
      // Set active page if specified
      if (activePage && PAGE_CONFIG[activePage]) {
        $(`a[href="${PAGE_CONFIG[activePage].href}"]`).addClass('bg-primary-50 text-primary-500');
      }
      
      // Initialize mobile menu toggle
      initializeMobileMenu();
      
      // Update evaluation counts after navigation is loaded
      updateEvaluationCounts();
    });
  });
}

/**
 * Update breadcrumb with current page title
 */
function updateStudentBreadcrumb(activePage) {
  // Map page identifiers to display titles
  const pageTitles = {
    'student-dashboard': 'Student Dashboard',
    'pending-evaluations': 'Pending Evaluations',
    'my-evaluations': 'My Evaluations',
    'evaluation-form': 'Evaluation Form',
    'my-profile': 'My Profile',
    'help-support': 'Help & Support',
    'settings': 'Settings'
  };
  
  const pageTitle = pageTitles[activePage] || 'Student Dashboard';
  
  // Update breadcrumb after a short delay to ensure header is loaded
  setTimeout(function() {
    const currentPageElement = document.getElementById('current-page');
    if (currentPageElement) {
      currentPageElement.textContent = pageTitle;
      console.log('Breadcrumb updated to:', pageTitle);
    }
  }, 100);
}

/**
 * Initialize mobile menu functionality
 */
function initializeMobileMenu() {
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  
  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', function() {
      sidebar.classList.toggle('-translate-x-full');
      if (overlay) {
        overlay.classList.toggle('hidden');
      }
    });
  }
  
  // Close sidebar when clicking overlay
  if (overlay) {
    overlay.addEventListener('click', function() {
      sidebar.classList.add('-translate-x-full');
      overlay.classList.add('hidden');
    });
  }
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
  const sidebar = document.getElementById('sidebar');
  const menuToggle = document.getElementById('menu-toggle');
  
  if (window.innerWidth < 1024 && 
      sidebar && menuToggle && 
      !sidebar.contains(event.target) && 
      !menuToggle.contains(event.target) &&
      !sidebar.classList.contains('-translate-x-full')) {
    sidebar.classList.add('-translate-x-full');
    
    const overlay = document.getElementById('sidebar-overlay');
    if (overlay) {
      overlay.classList.add('hidden');
    }
  }
});

/**
 * Update evaluation counts in navigation
 */
function updateEvaluationCounts() {
  fetch('/api/student/evaluation-counts')
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Update navigation pending count using the correct ID selector
        const navPendingBadge = document.getElementById('pending-count-badge');
        if (navPendingBadge) {
          navPendingBadge.textContent = data.pending_count;
          if (data.pending_count === 0) {
            navPendingBadge.className = 'ml-auto inline-flex items-center px-1.5 sm:px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800';
          } else {
            navPendingBadge.className = 'ml-auto inline-flex items-center px-1.5 sm:px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800';
          }
        }
      }
    })
    .catch(error => {
      console.error('Error updating evaluation counts:', error);
    });
}

/**
 * Standard Tailwind configuration for all student pages
 */
function getStandardTailwindConfig() {
  return {
    theme: {
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      extend: {
        colors: {
          primary: {
            50: '#e6f0ff',
            100: '#b3d1ff',
            200: '#80b3ff',
            300: '#4d94ff', 
            400: '#1a75ff',
            500: '#0059cc', // Primary color
            600: '#004db3',
            700: '#004099',
            800: '#003380',
            900: '#002766',
          },
          secondary: {
            50: '#f5f7fa',
            100: '#e4e7eb',
            200: '#cbd2d9',
            300: '#9aa5b1',
            400: '#7b8794',
            500: '#616e7c',
            600: '#52606d',
            700: '#3e4c59',
            800: '#323f4b',
            900: '#1f2933',
          },
        },
      }
    }
  };
}

/**
 * Standard CSS styles for all student pages
 */
function getStandardStyles() {
  return `
    /* Global styles */
    body {
      font-family: 'Inter', sans-serif;
      overflow-x: hidden;
    }
    
    /* Sidebar animation */
    @keyframes slideIn {
      from { transform: translateX(-100%); }
      to { transform: translateX(0); }
    }
    
    /* Dropdown animation */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    
    ::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
      background: #c1c1c1;
      border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
      background: #a8a8a8;
    }
    
    /* Card hover effect */
    .dashboard-card {
      transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Active nav link */
    .nav-link.active {
      position: relative;
    }
    
    .nav-link.active::after {
      content: '';
      position: absolute;
      left: 0;
      width: 4px;
      height: 100%;
      background-color: #0059cc;
      border-radius: 0 2px 2px 0;
    }
    
    /* Mobile responsive styles */
    @media (max-width: 768px) {
      .dashboard-card {
        margin-bottom: 1rem;
      }
      
      .lg\\:grid-cols-2 {
        grid-template-columns: repeat(1, minmax(0, 1fr)) !important;
      }
      
      .md\\:flex-row {
        flex-direction: column !important;
      }
      
      .md\\:items-center {
        align-items: flex-start !important;
      }
      
      .p-5.sm\\:p-6 {
        padding: 1rem !important;
      }
      
      .text-xl {
        font-size: 1.125rem !important;
        line-height: 1.75rem !important;
      }
      
      .overflow-x-auto {
        -webkit-overflow-scrolling: touch;
      }
    }
    
    @media (max-width: 640px) {
      .p-4.md\\:p-6 {
        padding: 0.75rem !important;
      }
      
      .gap-6 {
        gap: 1rem !important;
      }
      
      .mb-6 {
        margin-bottom: 1rem !important;
      }
      
      .text-lg {
        font-size: 1rem !important;
        line-height: 1.5rem !important;
      }
    }
  `;
}

/**
 * Fallback function to load academic year directly
 */
function loadAcademicYearFallback() {
  console.log('Loading academic year via fallback method...');
  
  const academicYearElement = document.getElementById('academic-year');
  if (!academicYearElement) {
    console.warn('Academic year element not found in DOM');
    return;
  }

  fetch('/api/academic-year')
    .then(response => {
      console.log('Fallback API Response status:', response.status);
      return response.json();
    })
    .then(data => {
      console.log('Fallback academic year API data:', data);
      
      if (data.success) {
        const displayText = data.display_text || `${data.year} - ${data.semester}`;
        academicYearElement.textContent = displayText;
        console.log('Academic year updated via fallback to:', displayText);
      } else {
        console.warn('Fallback API returned success: false');
        academicYearElement.textContent = '2025-2026 - 1st Semester';
      }
    })
    .catch(error => {
      console.error('Error in fallback academic year loading:', error);
      academicYearElement.textContent = '2025-2026 - 1st Semester';
    });
}