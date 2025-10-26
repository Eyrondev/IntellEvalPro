/**
 * Session Timeout Manager for IntellEvalPro
 * Monitors user session and automatically logs out after 1 hour of inactivity
 * Shows warning 5 minutes before timeout
 */

(function() {
    'use strict';
    
    // Configuration
    const SESSION_DURATION = 3600; // 1 hour in seconds
    const WARNING_TIME = 300; // Show warning 5 minutes before timeout
    const CHECK_INTERVAL = 30000; // Check session every 30 seconds
    const ACTIVITY_REFRESH_INTERVAL = 300000; // Refresh session every 5 minutes on activity
    
    let sessionCheckTimer = null;
    let warningShown = false;
    let lastActivityTime = Date.now();
    let warningModal = null;
    
    /**
     * Initialize session timeout monitoring
     */
    function init() {
        // Don't run on public/auth pages
        const publicPages = ['/login', '/signup', '/forgot-password', '/reset-password', '/logout'];
        const currentPath = window.location.pathname;
        
        if (publicPages.some(page => currentPath.includes(page))) {
            console.log('Session timeout: Skipping initialization on public page');
            return;
        }
        
        // Check if user is actually logged in
        if (!sessionStorage.getItem('is_logged_in')) {
            console.log('Session timeout: User not logged in, skipping');
            return;
        }
        
        // Create warning modal
        createWarningModal();
        
        // Start session checking
        startSessionCheck();
        
        // Track user activity
        trackUserActivity();
        
        console.log('Session timeout monitoring initialized (1 hour timeout)');
    }
    
    /**
     * Create the warning modal HTML
     */
    function createWarningModal() {
        const modalHTML = `
            <div id="session-timeout-modal" style="display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);">
                <div style="position: relative; margin: 15% auto; padding: 20px; width: 90%; max-width: 500px; background-color: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="text-align: center;">
                        <div style="font-size: 48px; color: #f59e0b; margin-bottom: 15px;">⏰</div>
                        <h2 style="margin: 0 0 15px 0; color: #1f2937; font-size: 24px;">Session Expiring Soon</h2>
                        <p style="color: #6b7280; margin-bottom: 20px;">
                            Your session will expire in <strong id="session-countdown" style="color: #ef4444;">5:00</strong> due to inactivity.
                        </p>
                        <p style="color: #6b7280; margin-bottom: 25px;">
                            Click "Stay Logged In" to continue your session, or you will be automatically logged out.
                        </p>
                        <div style="display: flex; gap: 10px; justify-content: center;">
                            <button id="session-extend-btn" style="padding: 10px 24px; background-color: #0059cc; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: 500;">
                                Stay Logged In
                            </button>
                            <button id="session-logout-btn" style="padding: 10px 24px; background-color: #6b7280; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px;">
                                Logout Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        warningModal = document.getElementById('session-timeout-modal');
        
        // Add event listeners
        document.getElementById('session-extend-btn').addEventListener('click', extendSession);
        document.getElementById('session-logout-btn').addEventListener('click', logoutNow);
    }
    
    /**
     * Start checking session status periodically
     */
    function startSessionCheck() {
        // Check immediately
        checkSessionStatus();
        
        // Then check every 30 seconds
        sessionCheckTimer = setInterval(checkSessionStatus, CHECK_INTERVAL);
    }
    
    /**
     * Check session status with the server
     */
    function checkSessionStatus() {
        fetch('/api/session-status', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                // Session expired or not authenticated
                handleSessionExpired();
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            
            if (data.success && data.logged_in) {
                const remainingSeconds = data.remaining_seconds;
                
                // Show warning if less than 5 minutes remaining
                if (remainingSeconds <= WARNING_TIME && !warningShown) {
                    showWarning(remainingSeconds);
                } else if (remainingSeconds > WARNING_TIME && warningShown) {
                    hideWarning();
                }
                
                // Update countdown if warning is shown
                if (warningShown) {
                    updateCountdown(remainingSeconds);
                }
            } else {
                handleSessionExpired();
            }
        })
        .catch(error => {
            console.error('Error checking session status:', error);
        });
    }
    
    /**
     * Show session expiration warning
     */
    function showWarning(remainingSeconds) {
        warningShown = true;
        warningModal.style.display = 'block';
        updateCountdown(remainingSeconds);
    }
    
    /**
     * Hide session expiration warning
     */
    function hideWarning() {
        warningShown = false;
        warningModal.style.display = 'none';
    }
    
    /**
     * Update countdown display
     */
    function updateCountdown(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        const countdownElement = document.getElementById('session-countdown');
        if (countdownElement) {
            countdownElement.textContent = `${minutes}:${secs.toString().padStart(2, '0')}`;
        }
    }
    
    /**
     * Handle session expiration
     */
    function handleSessionExpired() {
        clearInterval(sessionCheckTimer);
        
        // Clear session storage to prevent redirect loops
        sessionStorage.removeItem('is_logged_in');
        sessionStorage.removeItem('last_page');
        
        // Set session expired flag
        sessionStorage.setItem('session_expired', 'true');
        
        // Show alert
        alert('Your session has expired after 1 hour of inactivity. You will be redirected to the login page.');
        
        // Use replace to prevent back button issues
        window.location.replace('/login');
    }
    
    /**
     * Extend session when user clicks button
     */
    function extendSession() {
        fetch('/api/refresh-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                hideWarning();
                lastActivityTime = Date.now();
                
                // Show success message
                showToast('Session extended successfully!', 'success');
            }
        })
        .catch(error => {
            console.error('Error extending session:', error);
            showToast('Failed to extend session. Please try again.', 'error');
        });
    }
    
    /**
     * Logout immediately
     */
    function logoutNow() {
        window.location.href = '/logout';
    }
    
    /**
     * Track user activity and refresh session
     */
    function trackUserActivity() {
        const activityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
        
        activityEvents.forEach(event => {
            document.addEventListener(event, function() {
                const now = Date.now();
                
                // Refresh session if more than 5 minutes since last refresh
                if (now - lastActivityTime > ACTIVITY_REFRESH_INTERVAL) {
                    lastActivityTime = now;
                    
                    // Silently refresh session in background
                    fetch('/api/refresh-session', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        credentials: 'same-origin'
                    }).catch(error => {
                        console.error('Error refreshing session:', error);
                    });
                }
            }, { passive: true });
        });
    }
    
    /**
     * Show toast notification
     */
    function showToast(message, type = 'info') {
        // Check if SweetAlert2 is available
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                icon: type === 'success' ? 'success' : type === 'error' ? 'error' : 'info',
                title: message,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true
            });
        } else {
            // Fallback to alert
            alert(message);
        }
    }
    
    /**
     * Handle page visibility changes
     * Pause checking when tab is not visible to save resources
     */
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            // Page is hidden, but keep session check running
            // (session timeout continues even when tab is not visible)
        } else {
            // Page is visible again, check session immediately
            checkSessionStatus();
        }
    });
    
    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
