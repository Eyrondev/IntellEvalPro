/**
 * Prevent Logout on Browser Back Button
 * Simple and effective solution
 */

(function() {
    'use strict';
    
    // Don't run on public pages
    const publicPaths = ['/login', '/login.html', '/signup', '/forgot-password', '/reset-password'];
    const currentPath = window.location.pathname;
    
    if (publicPaths.some(path => currentPath.includes(path)) || currentPath === '/' || currentPath === '') {
        return;
    }
    
    console.log('🔒 Back button protection ACTIVE');
    
    // Mark as logged in
    sessionStorage.setItem('is_logged_in', 'true');
    sessionStorage.setItem('last_page', currentPath);
    
    // Get dashboard URL based on current path
    function getDashboardUrl() {
        if (currentPath.includes('/admin/')) return '/admin/admin-dashboard';
        if (currentPath.includes('/guidance/')) return '/guidance/guidance-dashboard';
        return '/student/student-dashboard';
    }
    
    // Prevent browser cache
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            console.log('⚠️ Page from cache, reloading');
            window.location.reload();
        }
    });
    
    // MAIN FIX: Block back to logout/login
    window.addEventListener('popstate', function(event) {
        const path = window.location.pathname;
        console.log('⬅️ Back button pressed, path:', path);
        
        // Check if session expired - if so, allow navigation to login
        const sessionExpired = sessionStorage.getItem('session_expired');
        if (sessionExpired === 'true') {
            console.log('⏱️ Session expired, allowing navigation to login');
            return;
        }
        
        if ((path.includes('/logout') || path.includes('/login')) && 
            sessionStorage.getItem('is_logged_in') === 'true') {
            
            console.log('🚫 BLOCKED back to logout/login');
            event.preventDefault();
            event.stopPropagation();
            
            const lastPage = sessionStorage.getItem('last_page');
            const redirectTo = (lastPage && !lastPage.includes('/logout') && !lastPage.includes('/login')) 
                ? lastPage : getDashboardUrl();
            
            console.log('↪️ Redirecting to:', redirectTo);
            
            // Use replace to avoid adding to history
            window.location.replace(redirectTo);
            return false;
        }
    });
    
    // Auto-refresh session every 5 minutes on activity
    let lastRefresh = Date.now();
    const events = ['mousedown', 'keydown', 'scroll', 'touchstart'];
    
    events.forEach(function(eventName) {
        document.addEventListener(eventName, function() {
            const now = Date.now();
            if (now - lastRefresh > 300000) { // 5 minutes
                lastRefresh = now;
                fetch('/api/refresh-session', { 
                    method: 'POST', 
                    credentials: 'same-origin' 
                }).catch(function(err) {
                    console.error('Session refresh error:', err);
                });
            }
        }, { passive: true });
    });
    
    console.log('✅ Protection initialized successfully');
    
})();
