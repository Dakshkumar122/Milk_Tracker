// ========== SPLASH SCREEN FUNCTIONALITY ==========
document.addEventListener('DOMContentLoaded', function() {
    // Create splash screen element
    var splashHTML = `
        <div class="splash-screen" id="splashScreen">
            <div class="splash-content">
                <div class="splash-logo">
                    <i class="fas fa-tint"></i>
                </div>
                <div class="splash-title">
                    Milk Tracker Pro
                </div>
                <div class="splash-subtitle">
                    Smart Dairy Management System
                </div>
                <div class="loader"></div>
            </div>
        </div>
    `;
    
    // Insert splash screen at the beginning of body
    document.body.insertAdjacentHTML('afterbegin', splashHTML);
    
    // Hide main content initially
    var mainContent = document.querySelector('.container');
    if (mainContent) {
        mainContent.style.display = 'none';
    }
    
    // Show splash screen for 2.5 seconds, then hide and show main content
    setTimeout(function() {
        var splash = document.getElementById('splashScreen');
        if (splash) {
            splash.classList.add('hide');
            setTimeout(function() {
                splash.remove();
            }, 500);
        }
        
        // Show main content
        if (mainContent) {
            mainContent.style.display = 'block';
            mainContent.classList.add('show');
        }
    }, 2500);
});

// ========== AUTO-SUBMIT FILTER ==========
document.addEventListener('DOMContentLoaded', function() {
    var selects = document.querySelectorAll('select[name="month"], select[name="year"]');
    for (var i = 0; i < selects.length; i++) {
        selects[i].addEventListener('change', function() {
            var form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
});

// ========== AUTO-HIDE MESSAGES ==========
document.addEventListener('DOMContentLoaded', function() {
    var messages = document.querySelectorAll('.alert-premium');
    for (var i = 0; i < messages.length; i++) {
        (function(msg) {
            setTimeout(function() {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s';
                setTimeout(function() {
                    if (msg.parentElement) {
                        msg.remove();
                    }
                }, 500);
            }, 3000);
        })(messages[i]);
    }
    
    // Close button for messages
    var closeBtns = document.querySelectorAll('.close-btn');
    for (var i = 0; i < closeBtns.length; i++) {
        closeBtns[i].addEventListener('click', function() {
            var parent = this.parentElement;
            if (parent) {
                parent.remove();
            }
        });
    }
});