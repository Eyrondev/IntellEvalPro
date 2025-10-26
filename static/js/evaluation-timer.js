/**
 * Evaluation Timer Class
 * Manages persistent timer with localStorage + server validation
 * Automatically expires evaluation when time runs out
 * 
 * Features:
 * - Persists across page refresh
 * - Survives logout/login
 * - Server-side time validation
 * - Auto-submit on expiration
 * - Visual warnings at intervals
 */

class EvaluationTimer {
  constructor(sessionId, startTime, timeLimitMinutes) {
    this.sessionId = sessionId;
    this.startTime = new Date(startTime);
    this.timeLimitSeconds = timeLimitMinutes * 60;
    this.timerInterval = null;
    this.syncInterval = null;
    this.isExpired = false;
    this.warningShown = false;
    this.finalWarningShown = false;
    
    // Try to restore from localStorage
    this.restoreFromStorage();
    
    // Start timer
    this.start();
  }
  
  /**
   * Save timer state to localStorage
   */
  saveToStorage() {
    const timerData = {
      sessionId: this.sessionId,
      startTime: this.startTime.toISOString(),
      timeLimitSeconds: this.timeLimitSeconds
    };
    localStorage.setItem('evaluationTimer', JSON.stringify(timerData));
  }
  
  /**
   * Restore timer state from localStorage
   */
  restoreFromStorage() {
    const stored = localStorage.getItem('evaluationTimer');
    if (stored) {
      try {
        const data = JSON.parse(stored);
        if (data.sessionId === this.sessionId) {
          this.startTime = new Date(data.startTime);
          this.timeLimitSeconds = data.timeLimitSeconds;
          console.log('✅ Timer restored from localStorage');
        }
      } catch (e) {
        console.error('Failed to restore timer:', e);
      }
    }
  }
  
  /**
   * Calculate remaining time in seconds
   */
  getRemainingSeconds() {
    const now = new Date();
    const elapsed = Math.floor((now - this.startTime) / 1000);
    const remaining = this.timeLimitSeconds - elapsed;
    return Math.max(0, remaining);
  }
  
  /**
   * Format time as MM:SS
   */
  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  /**
   * Update timer display
   */
  updateDisplay() {
    const remaining = this.getRemainingSeconds();
    const formatted = this.formatTime(remaining);
    
    // Update timer element
    const timerElement = document.getElementById('evaluation-timer');
    if (timerElement) {
      timerElement.textContent = formatted;
      
      // Remove previous warning classes
      timerElement.classList.remove('text-red-600', 'text-yellow-600', 'text-gray-900', 'font-bold', 'animate-pulse');
      
      // Apply warning styles based on remaining time
      if (remaining === 0) {
        timerElement.classList.add('text-red-600', 'font-bold');
        timerElement.textContent = 'EXPIRED';
      } else if (remaining <= 60) {
        // Last minute - red and pulsing
        timerElement.classList.add('text-red-600', 'font-bold', 'animate-pulse');
      } else if (remaining <= 300) {
        // Last 5 minutes - yellow warning
        timerElement.classList.add('text-yellow-600', 'font-bold');
      } else {
        // Normal time - gray
        timerElement.classList.add('text-gray-900');
      }
    }
    
    // Update progress bar if exists
    const progressBar = document.getElementById('timer-progress-bar');
    if (progressBar) {
      const percentage = (remaining / this.timeLimitSeconds) * 100;
      progressBar.style.width = `${percentage}%`;
      
      // Change color based on time remaining
      progressBar.classList.remove('bg-primary-600', 'bg-yellow-500', 'bg-red-600');
      if (remaining <= 60) {
        progressBar.classList.add('bg-red-600');
      } else if (remaining <= 300) {
        progressBar.classList.add('bg-yellow-500');
      } else {
        progressBar.classList.add('bg-primary-600');
      }
    }
    
    // Show warning at 5 minutes
    if (remaining === 300 && !this.warningShown) {
      this.warningShown = true;
      Swal.fire({
        icon: 'warning',
        title: '5 Minutes Remaining',
        text: 'You have 5 minutes left to complete this evaluation.',
        timer: 3000,
        timerProgressBar: true,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
      });
    }
    
    // Show final warning at 1 minute
    if (remaining === 60 && !this.finalWarningShown) {
      this.finalWarningShown = true;
      Swal.fire({
        icon: 'error',
        title: '1 Minute Remaining!',
        text: 'Please submit your evaluation soon.',
        timer: 5000,
        timerProgressBar: true,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
      });
    }
    
    // Time expired
    if (remaining === 0 && !this.isExpired) {
      this.handleTimeout();
    }
  }
  
  /**
   * Sync with server to validate time
   */
  async syncWithServer() {
    try {
      const response = await fetch(`/api/evaluation/check-time/${this.sessionId}`);
      const data = await response.json();
      
      if (data.success) {
        // Check if server says it's expired
        if (data.status === 'expired') {
          this.handleTimeout();
          return;
        }
        
        // Detect time manipulation (client vs server difference > 5 seconds)
        const clientRemaining = this.getRemainingSeconds();
        const serverRemaining = data.remaining_seconds;
        
        if (Math.abs(clientRemaining - serverRemaining) > 5) {
          console.warn('⚠️ Time mismatch detected, syncing with server');
          console.log(`Client: ${clientRemaining}s, Server: ${serverRemaining}s`);
          
          // Recalculate start time based on server data
          const now = new Date();
          this.startTime = new Date(now - (data.elapsed_seconds * 1000));
          this.saveToStorage();
          this.updateDisplay();
        }
      }
    } catch (error) {
      console.error('Failed to sync with server:', error);
    }
  }
  
  /**
   * Handle timeout - show expired UI and discard responses
   */
  handleTimeout() {
    if (this.isExpired) return; // Prevent multiple calls
    
    this.isExpired = true;
    this.stop();
    
    // Clear all form inputs (discard responses)
    this.clearAllResponses();
    
    // Disable all form inputs
    this.disableForm();
    
    // Show expired overlay
    this.showExpiredOverlay();
    
    // Show SweetAlert notification
    Swal.fire({
      icon: 'error',
      title: 'Time Expired',
      html: `
        <p class="text-base">Your evaluation time has expired.</p>
        <p class="text-sm text-red-600 mt-2 font-semibold">Your responses have been discarded.</p>
        <p class="text-xs text-gray-600 mt-2">Please contact your instructor if you need to retake this evaluation.</p>
      `,
      allowOutsideClick: false,
      showConfirmButton: true,
      confirmButtonText: 'Return to Dashboard',
      confirmButtonColor: '#ef4444',
      showCancelButton: false
    }).then(() => {
      // Mark evaluation as expired (no submission)
      this.markAsExpired();
    });
  }
  
  /**
   * Clear all form responses
   */
  clearAllResponses() {
    // Uncheck all radio buttons
    document.querySelectorAll('input[type="radio"]').forEach(input => {
      input.checked = false;
    });
    
    // Clear all textareas
    document.querySelectorAll('textarea').forEach(textarea => {
      textarea.value = '';
    });
    
    // Clear all text inputs
    document.querySelectorAll('input[type="text"]').forEach(input => {
      input.value = '';
    });
    
    // Reset all select elements
    document.querySelectorAll('select').forEach(select => {
      select.selectedIndex = 0;
    });
    
    console.log('✅ All responses cleared due to timeout');
  }
  
  /**
   * Disable form inputs
   */
  disableForm() {
    // Disable all radio buttons
    document.querySelectorAll('input[type="radio"]').forEach(input => {
      input.disabled = true;
    });
    
    // Disable all textareas
    document.querySelectorAll('textarea').forEach(textarea => {
      textarea.disabled = true;
    });
    
    // Disable all select elements
    document.querySelectorAll('select').forEach(select => {
      select.disabled = true;
    });
    
    // Disable submit button
    const submitBtn = document.getElementById('submit-evaluation');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    }
  }
  
  /**
   * Show expired overlay on form
   */
  showExpiredOverlay() {
    const expiredOverlay = document.createElement('div');
    expiredOverlay.id = 'expired-overlay';
    expiredOverlay.className = 'fixed inset-0 bg-black bg-opacity-50 z-40 flex items-center justify-center p-4';
    expiredOverlay.innerHTML = `
      <div class="bg-white rounded-lg shadow-xl p-6 sm:p-8 max-w-md w-full mx-auto text-center animate-fadeIn">
        <div class="mb-4">
          <i class="fas fa-clock text-5xl sm:text-6xl text-red-500 mb-4 animate-pulse"></i>
        </div>
        <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-2">Evaluation Expired</h2>
        <p class="text-sm sm:text-base text-gray-600 mb-4">
          Your time limit has been reached. The evaluation form is now closed.
        </p>
        <div class="bg-red-50 border-l-4 border-red-400 p-4 mb-4 text-left">
          <p class="text-xs sm:text-sm text-red-800">
            <i class="fas fa-exclamation-triangle mr-2"></i>
            Your responses have been discarded. Please contact your instructor to retake this evaluation.
          </p>
        </div>
        <button onclick="location.href='/student/dashboard'" class="w-full px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors text-sm sm:text-base font-medium">
          <i class="fas fa-arrow-left mr-2"></i>
          Return to Dashboard
        </button>
      </div>
    `;
    
    document.body.appendChild(expiredOverlay);
  }
  
  /**
   * Mark evaluation as expired (no submission)
   */
  async markAsExpired() {
    try {
      const response = await fetch('/api/evaluation/mark-expired', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: this.sessionId
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        console.log('✅ Evaluation marked as expired');
        // Clear localStorage
        localStorage.removeItem('evaluationTimer');
        // Redirect to dashboard
        setTimeout(() => {
          window.location.href = '/student/dashboard';
        }, 2000);
      } else {
        console.error('Failed to mark as expired:', data.message);
        // Still redirect to dashboard
        setTimeout(() => {
          window.location.href = '/student/dashboard';
        }, 2000);
      }
    } catch (error) {
      console.error('Error marking evaluation as expired:', error);
      // Still redirect to dashboard
      setTimeout(() => {
        window.location.href = '/student/dashboard';
      }, 2000);
    }
  }
  
  /*
   * DEPRECATED: Auto-submit functionality removed
   * Timer expiration now discards responses instead of submitting
   */
  
  // /**
  //  * Auto-submit evaluation (DEPRECATED - NO LONGER USED)
  //  */
  // async autoSubmit() {
  //   // This function is no longer used
  //   // Responses are now discarded on timeout instead of auto-submitted
  // }
  
  // /**
  //  * Collect form responses (DEPRECATED - NO LONGER USED)
  //  */
  // collectResponses() {
  //   // This function is no longer used
  //   // Responses are cleared on timeout instead
  // }
  
  /**
   * Start timer
   */
  start() {
    // Save to localStorage
    this.saveToStorage();
    
    // Update display immediately
    this.updateDisplay();
    
    // Update every second
    this.timerInterval = setInterval(() => {
      this.updateDisplay();
    }, 1000);
    
    // Sync with server every 30 seconds
    this.syncInterval = setInterval(() => {
      this.syncWithServer();
    }, 30000);
    
    // Initial sync after 2 seconds
    setTimeout(() => {
      this.syncWithServer();
    }, 2000);
    
    // Warn before leaving page
    window.addEventListener('beforeunload', this.handleBeforeUnload.bind(this));
    
    console.log('✅ Evaluation timer started');
  }
  
  /**
   * Stop timer
   */
  stop() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
    }
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
    console.log('🛑 Evaluation timer stopped');
  }
  
  /**
   * Warn user before leaving
   */
  handleBeforeUnload(e) {
    const remaining = this.getRemainingSeconds();
    if (remaining > 0 && !this.isExpired) {
      e.preventDefault();
      e.returnValue = 'Your evaluation is in progress. Are you sure you want to leave?';
      return e.returnValue;
    }
  }
}

// Global timer instance
let evaluationTimer;

/**
 * Initialize evaluation timer
 * @param {number} evaluationId - The evaluation ID
 */
async function startEvaluation(evaluationId) {
  try {
    const response = await fetch('/api/evaluation/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ evaluation_id: evaluationId })
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Check if timer is disabled
      if (data.timer_enabled === false) {
        // Hide timer widget completely
        const timerWidget = document.getElementById('timer-widget');
        if (timerWidget) {
          timerWidget.style.display = 'none';
        }
        
        // Show notification that timer is disabled
        Swal.fire({
          icon: 'info',
          title: 'No Time Limit',
          text: data.message || 'You have unlimited time to complete this evaluation.',
          timer: 3000,
          showConfirmButton: false,
          toast: true,
          position: 'top-end'
        });
        
        return; // Exit - no timer to start
      }
      
      // Timer is enabled - start the timer
      evaluationTimer = new EvaluationTimer(
        data.session_id,
        data.start_time,
        data.time_limit
      );
      
      if (data.resumed) {
        Swal.fire({
          icon: 'info',
          title: 'Session Resumed',
          text: 'Your previous evaluation session has been resumed.',
          timer: 2000,
          showConfirmButton: false,
          toast: true,
          position: 'top-end'
        });
      }
    } else if (data.expired) {
      // Show expired state immediately
      Swal.fire({
        icon: 'error',
        title: 'Session Expired',
        text: 'Your previous evaluation session has expired. Please contact your instructor.',
        confirmButtonColor: '#0059cc'
      }).then(() => {
        window.location.href = '/student/dashboard';
      });
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: data.error || 'Failed to start evaluation',
        confirmButtonColor: '#0059cc'
      });
    }
  } catch (error) {
    console.error('Failed to start evaluation:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to start evaluation. Please try again.',
      confirmButtonColor: '#0059cc'
    });
  }
}
