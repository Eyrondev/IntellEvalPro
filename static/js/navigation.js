// IntellEvalPro Navigation Configuration
// This file manages the navigation connections between different sections of the application

/**
 * Navigation Configuration
 * Contains definitions for all navigation components in the application
 */

// Define all available pages in the system
const systemPages = {
  // Authentication Pages
  auth: {
    login: '/login.html',
    signup: '/signup.html',
    forgotPassword: '/forgot-password.html',
    resetPassword: '/reset-password.html'
  },
  
  // Dashboard Pages
  dashboard: {
    admin: '/admin-dashboard.html',
    student: '/student-dashboard.html',
    guidance: '/guidance-dashboard.html'
  },
  
  // Admin Section
  admin: {
    users: '/admin/user-management.html',
    departments: '/admin/departments.html',
    courses: '/admin/courses.html',
    evaluationForms: '/admin/evaluation-forms.html',
    evaluationPeriods: '/admin/evaluation-periods.html',
    settings: '/admin/system-settings.html',
    logs: '/admin/logs.html'
  },
  
  // Faculty Section (removed - faculty role deprecated)
  
  // Student Section
  student: {
    home: '/student/home.html',
    pendingEvaluations: '/student/pending-evaluations.html',
    completedEvaluations: '/student/completed-evaluations.html'
  },
  
  // Dean Section (removed - dean role deprecated)
  
  // Guidance Section
  guidance: {
    home: '/guidance/home.html',
    improvementPlans: '/guidance/improvement-plans.html',
    facultyCoaching: '/guidance/faculty-coaching.html',
    workshops: '/guidance/workshops.html'
  },
  
  // System Documentation
  documentation: {
    database: '/database/database-documentation.html',
    userGuide: '/docs/user-guide.html',
    apiDocumentation: '/docs/api-documentation.html'
  },
  
  // Common Pages
  common: {
    profile: '/profile.html',
    notifications: '/notifications.html',
    helpCenter: '/help-center.html'
  }
};

/**
 * Navigation Menu Definitions
 * Defines the navigation menus for different user roles
 */
const navigationMenus = {
  // Admin Navigation
  adminMenu: [
    {
      label: 'Dashboard',
      icon: 'fas fa-gauge-high',
      url: systemPages.dashboard.admin
    },
    {
      label: 'User Management',
      icon: 'fas fa-users-gear',
      url: systemPages.admin.users
    },
    {
      label: 'Departments',
      icon: 'fas fa-building-user',
      url: systemPages.admin.departments
    },
    {
      label: 'Courses',
      icon: 'fas fa-book',
      url: systemPages.admin.courses
    },
    {
      label: 'Evaluation Forms',
      icon: 'fas fa-clipboard-list',
      url: systemPages.admin.evaluationForms
    },
    {
      label: 'Evaluation Periods',
      icon: 'fas fa-calendar-days',
      url: systemPages.admin.evaluationPeriods
    },
    {
      label: 'System Settings',
      icon: 'fas fa-sliders',
      url: systemPages.admin.settings
    },
    {
      label: 'Database Schema',
      icon: 'fas fa-database',
      url: systemPages.documentation.database
    },
    {
      label: 'System Logs',
      icon: 'fas fa-list-check',
      url: systemPages.admin.logs
    }
  ],
  
  // Faculty Navigation (removed)
  
  // Student Navigation
  studentMenu: [
    {
      label: 'Dashboard',
      icon: 'fas fa-gauge-high',
      url: systemPages.student.home
    },
    {
      label: 'Pending Evaluations',
      icon: 'fas fa-clock',
      url: systemPages.student.pendingEvaluations
    },
    {
      label: 'Completed Evaluations',
      icon: 'fas fa-check-circle',
      url: systemPages.student.completedEvaluations
    }
  ],
  
  // Dean Navigation (removed)
  
  // Guidance Navigation
  guidanceMenu: [
    {
      label: 'Dashboard',
      icon: 'fas fa-gauge-high',
      url: systemPages.guidance.home
    },
    {
      label: 'Improvement Plans',
      icon: 'fas fa-arrows-to-circle',
      url: systemPages.guidance.improvementPlans
    },
    {
      label: 'Faculty Coaching',
      icon: 'fas fa-people-arrows',
      url: systemPages.guidance.facultyCoaching
    },
    {
      label: 'Workshops',
      icon: 'fas fa-chalkboard',
      url: systemPages.guidance.workshops
    }
  ]
};

/**
 * User Menu (Profile Dropdown) - Common across roles
 */
const userMenu = [
  {
    label: 'My Profile',
    icon: 'fas fa-user',
    url: systemPages.common.profile
  },
  {
    label: 'Notifications',
    icon: 'fas fa-bell',
    url: systemPages.common.notifications
  },
  {
    label: 'Help Center',
    icon: 'fas fa-circle-question',
    url: systemPages.common.helpCenter
  },
  {
    label: 'Logout',
    icon: 'fas fa-arrow-right-from-bracket',
    url: systemPages.auth.login,
    class: 'text-red-600 hover:bg-red-50'
  }
];

/**
 * Function to render the navigation menu based on user role
 * @param {string} role - The user role (admin, faculty, student, dean, guidance)
 * @param {string} currentPage - The current page path for highlighting active item
 * @returns {string} HTML string for the navigation menu
 */
function renderNavigation(role, currentPage) {
  let menuItems = [];
  
  // Select the appropriate menu based on role
  switch(role) {
    case 'admin':
      menuItems = navigationMenus.adminMenu;
      break;
    case 'student':
      menuItems = navigationMenus.studentMenu;
      break;
    case 'guidance':
      menuItems = navigationMenus.guidanceMenu;
      break;
    default:
      menuItems = [];
  }
  
  // Generate the HTML for menu items
  let html = '';
  menuItems.forEach(item => {
    const isActive = currentPage === item.url;
    html += `
      <li>
        <a href="${item.url}" class="nav-link ${isActive ? 'active' : ''} flex items-center px-4 py-2.5 text-sm font-medium text-gray-900 rounded-lg hover:bg-gray-100 group transition-all duration-200 ${isActive ? 'bg-gray-100' : ''}">
          <i class="${item.icon} w-5 h-5 text-primary-500 mr-2.5"></i>
          <span>${item.label}</span>
        </a>
      </li>
    `;
  });
  
  return html;
}

/**
 * Function to render the user dropdown menu
 * @param {string} currentPage - The current page path for highlighting active item
 * @returns {string} HTML string for the user dropdown menu
 */
function renderUserMenu(currentPage) {
  let html = '';
  userMenu.forEach(item => {
    const isActive = currentPage === item.url;
    html += `
      <a href="${item.url}" class="${item.class || ''} flex items-center px-4 py-3 text-sm ${isActive ? 'bg-gray-100' : 'hover:bg-gray-100'} transition-colors duration-200">
        <i class="${item.icon} w-5 h-5 mr-3"></i>
        ${item.label}
      </a>
    `;
  });
  
  return html;
}

/**
 * Initialize navigation for the current page
 * @param {string} role - The user role
 * @param {string} currentPage - The current page path
 */
function initializeNavigation(role, currentPage) {
  // Render role-specific menu
  const roleMenuContainer = document.getElementById('role-specific-menu');
  if (roleMenuContainer) {
    roleMenuContainer.innerHTML = renderNavigation(role, currentPage);
  }
  
  // Render user dropdown when button is clicked
  const userMenuButton = document.getElementById('user-menu-button');
  const userMenuDropdown = document.getElementById('user-menu-dropdown');
  
  if (userMenuButton && userMenuDropdown) {
    // Populate the dropdown
    userMenuDropdown.innerHTML = renderUserMenu(currentPage);
    
    // Toggle dropdown visibility
    userMenuButton.addEventListener('click', () => {
      userMenuDropdown.classList.toggle('hidden');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (event) => {
      if (!userMenuButton.contains(event.target) && !userMenuDropdown.contains(event.target)) {
        userMenuDropdown.classList.add('hidden');
      }
    });
  }
}

// Export for use in other modules
if (typeof module !== 'undefined') {
  module.exports = {
    systemPages,
    navigationMenus,
    userMenu,
    renderNavigation,
    renderUserMenu,
    initializeNavigation
  };
}
