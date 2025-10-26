/**
 * Loading Animation Module
 * Provides reusable loading overlay functionality for IntellEvalPro
 */

/**
 * Initialize and show loading overlay
 */
function showLoadingOverlay() {
  // Create loading overlay if it doesn't exist
  if (!document.getElementById('loader-overlay')) {
    const overlay = document.createElement('div');
    overlay.id = 'loader-overlay';
    overlay.className = 'fixed inset-0 z-50 flex flex-col items-center justify-center bg-white bg-opacity-90 backdrop-blur-sm transition-opacity duration-300';
    
    // Use absolute path for logo (works in all contexts)
    const logoPath = '/static/images/nclogo.png';
    
    overlay.innerHTML = `
      <img src="${logoPath}" alt="Logo" class="w-32 h-auto mb-6 animate-bounce">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-primary-500 animate-pulse"></div>
        <div class="w-3 h-3 rounded-full bg-primary-500 animate-pulse" style="animation-delay: 0.2s"></div>
        <div class="w-3 h-3 rounded-full bg-primary-500 animate-pulse" style="animation-delay: 0.4s"></div>
      </div>
    `;
    
    document.body.appendChild(overlay);
  }
  
  const overlay = document.getElementById('loader-overlay');
  overlay.style.display = 'flex';
  overlay.style.opacity = '1';
}

/**
 * Hide loading overlay with smooth animation
 * @param {number} delay - Delay before hiding (default: 500ms)
 */
function hideLoadingOverlay(delay = 500) {
  const overlay = document.getElementById('loader-overlay');
  if (overlay) {
    setTimeout(function() {
      overlay.style.opacity = '0';
      setTimeout(() => {
        overlay.style.display = 'none';
      }, 300);
    }, delay);
  }
}

/**
 * Initialize loading animation when page starts loading
 */
function initializeLoadingAnimation() {
  // Show loading overlay immediately
  showLoadingOverlay();
  
  // Hide loader when page is ready
  window.addEventListener('load', function() {
    hideLoadingOverlay(500);
  });
  
  // Fallback: Hide loader after maximum wait time
  setTimeout(function() {
    hideLoadingOverlay(0);
  }, 5000);
}

/**
 * Create a custom loading spinner for specific elements
 * @param {string} containerId - ID of container to show spinner in
 * @param {string} message - Optional loading message
 */
function showElementSpinner(containerId, message = 'Loading...') {
  const container = document.getElementById(containerId);
  if (container) {
    const spinner = document.createElement('div');
    spinner.className = 'flex flex-col items-center justify-center p-8 min-h-[200px]';
    spinner.innerHTML = `
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mb-4"></div>
      <p class="text-sm text-gray-500">${message}</p>
    `;
    
    container.innerHTML = '';
    container.appendChild(spinner);
  }
}

/**
 * Show loading state for buttons
 * @param {string} buttonId - ID of button to show loading state
 * @param {string} loadingText - Text to show while loading
 */
function showButtonLoading(buttonId, loadingText = 'Loading...') {
  const button = document.getElementById(buttonId);
  if (button) {
    // Store original state
    button.dataset.originalText = button.innerHTML;
    button.dataset.originalDisabled = button.disabled;
    
    // Set loading state
    button.disabled = true;
    button.innerHTML = `
      <div class="flex items-center justify-center">
        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
        ${loadingText}
      </div>
    `;
  }
}

/**
 * Hide loading state for buttons
 * @param {string} buttonId - ID of button to restore
 */
function hideButtonLoading(buttonId) {
  const button = document.getElementById(buttonId);
  if (button && button.dataset.originalText) {
    button.innerHTML = button.dataset.originalText;
    button.disabled = button.dataset.originalDisabled === 'true';
    
    // Clean up data attributes
    delete button.dataset.originalText;
    delete button.dataset.originalDisabled;
  }
}

/**
 * Show skeleton loading for tables or lists
 * @param {string} containerId - ID of container to show skeleton in
 * @param {number} rows - Number of skeleton rows to show
 */
function showSkeletonLoading(containerId, rows = 5) {
  const container = document.getElementById(containerId);
  if (container) {
    let skeletonHTML = '';
    for (let i = 0; i < rows; i++) {
      skeletonHTML += `
        <div class="animate-pulse flex space-x-4 p-4 border-b border-gray-200">
          <div class="rounded-full bg-gray-300 h-10 w-10"></div>
          <div class="flex-1 space-y-2 py-1">
            <div class="h-4 bg-gray-300 rounded w-3/4"></div>
            <div class="h-4 bg-gray-300 rounded w-1/2"></div>
          </div>
        </div>
      `;
    }
    
    container.innerHTML = `
      <div class="bg-white rounded-lg border border-gray-200">
        ${skeletonHTML}
      </div>
    `;
  }
}

// Auto-initialize if this script is loaded
if (document.readyState === 'loading') {
  // DOM is still loading
  document.addEventListener('DOMContentLoaded', initializeLoadingAnimation);
} else {
  // DOM is already loaded
  initializeLoadingAnimation();
}