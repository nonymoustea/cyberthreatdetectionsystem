// Main JavaScript for AI Email Threat Detector

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var alertInstance = new bootstrap.Alert(alert);
            alertInstance.close();
        });
    }, 5000);

    // Add loading animation to buttons on form submission
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                var originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                
                // Re-enable button after 30 seconds (fallback)
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 30000);
            }
        });
    });
});

// Dashboard Statistics Updates
function updateDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalFiles').textContent = data.total_files;
            document.getElementById('phishingCount').textContent = data.phishing_count;
            document.getElementById('legitimateCount').textContent = data.legitimate_count;
            document.getElementById('phishingRate').textContent = data.phishing_rate + '%';
        })
        .catch(error => console.error('Error fetching stats:', error));
}

// Recent Analyses Updates
function updateRecentAnalyses() {
    fetch('/api/recent')
        .then(response => response.json())
        .then(data => {
            var recentAnalysesContainer = document.getElementById('recentAnalyses');
            if (recentAnalysesContainer && data.length > 0) {
                var html = '';
                data.forEach(function(analysis) {
                    var badgeClass = analysis.result === 'Phishing' ? 'bg-danger' : 'bg-success';
                    var icon = analysis.result === 'Phishing' ? 'exclamation-triangle' : 'check-circle';
                    var threatBadge = analysis.threat_level === 'HIGH' ? 'bg-danger' : 'bg-success';
                    
                    html += `
                        <tr>
                            <td><i class="fas fa-file me-2"></i>${analysis.filename}</td>
                            <td><span class="badge ${badgeClass}"><i class="fas fa-${icon} me-1"></i>${analysis.result}</span></td>
                            <td><span class="badge ${threatBadge}">${analysis.threat_level}</span></td>
                            <td><small class="text-muted">${analysis.timestamp.substring(0, 19).replace('T', ' ')}</small></td>
                            <td><a href="/result/${analysis.id}" class="btn btn-sm btn-outline-primary"><i class="fas fa-eye me-1"></i>View</a></td>
                        </tr>
                    `;
                });
                recentAnalysesContainer.innerHTML = html;
            }
        })
        .catch(error => console.error('Error fetching recent analyses:', error));
}

// File Upload Handling
function handleFileUpload() {
    var fileInput = document.getElementById('file');
    var filePreview = document.getElementById('filePreview');
    var previewContent = document.getElementById('previewContent');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            
            if (file) {
                // Show file preview
                if (filePreview) {
                    filePreview.style.display = 'block';
                    
                    // Get file icon based on type
                    var fileIcon = getFileIcon(file.name);
                    var fileSize = (file.size / 1024 / 1024).toFixed(2);
                    
                    if (previewContent) {
                        previewContent.innerHTML = `
                            <div class="d-flex align-items-center">
                                ${fileIcon}
                                <div class="ms-3">
                                    <strong>${file.name}</strong><br>
                                    <small class="text-muted">Size: ${fileSize} MB | Type: ${file.type || 'Unknown'}</small>
                                </div>
                                <div class="ms-auto">
                                    <span class="badge bg-primary">Ready for Analysis</span>
                                </div>
                            </div>
                        `;
                    }
                }
                
                // Validate file size
                if (file.size > 16 * 1024 * 1024) { // 16MB
                    showAlert('File size exceeds 16MB limit. Please choose a smaller file.', 'error');
                    fileInput.value = '';
                    if (filePreview) filePreview.style.display = 'none';
                    return;
                }
                
                // Validate file type
                var allowedTypes = ['text/plain', 'application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/bmp'];
                var allowedExtensions = ['.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.bmp'];
                var fileName = file.name.toLowerCase();
                var isValidType = allowedTypes.includes(file.type) || 
                                 allowedExtensions.some(ext => fileName.endsWith(ext));
                
                if (!isValidType) {
                    showAlert('Invalid file type. Please upload TXT, PDF, or image files only.', 'error');
                    fileInput.value = '';
                    if (filePreview) filePreview.style.display = 'none';
                    return;
                }
                
            } else {
                if (filePreview) filePreview.style.display = 'none';
            }
        });
    }
}

// Get appropriate file icon
function getFileIcon(filename) {
    var extension = filename.split('.').pop().toLowerCase();
    
    switch (extension) {
        case 'pdf':
            return '<i class="fas fa-file-pdf fa-3x text-danger"></i>';
        case 'png':
        case 'jpg':
        case 'jpeg':
        case 'gif':
        case 'bmp':
            return '<i class="fas fa-image fa-3x text-success"></i>';
        case 'txt':
            return '<i class="fas fa-file-alt fa-3x text-primary"></i>';
        default:
            return '<i class="fas fa-file fa-3x text-secondary"></i>';
    }
}

// Show custom alert
function showAlert(message, type = 'info') {
    var alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
    var icon = type === 'error' ? 'exclamation-triangle' : 
              type === 'success' ? 'check-circle' : 'info-circle';
    
    var alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas fa-${icon} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    var container = document.querySelector('.container .mt-4') || document.querySelector('.container');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-hide after 5 seconds
        setTimeout(function() {
            var alert = container.querySelector('.alert:first-child');
            if (alert) {
                var alertInstance = new bootstrap.Alert(alert);
                alertInstance.close();
            }
        }, 5000);
    }
}

// Copy to clipboard functionality
function copyToClipboard(text, element = null) {
    navigator.clipboard.writeText(text).then(function() {
        if (element) {
            var originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-check"></i> Copied!';
            element.classList.add('btn-success');
            
            setTimeout(function() {
                element.innerHTML = originalText;
                element.classList.remove('btn-success');
            }, 2000);
        }
        showAlert('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        showAlert('Failed to copy to clipboard', 'error');
    });
}

// Search functionality for tables
function initializeTableSearch() {
    var searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            var searchTerm = this.value.toLowerCase();
            var rows = document.querySelectorAll('.analysis-row');
            
            rows.forEach(function(row) {
                var filename = row.querySelector('.filename');
                if (filename) {
                    var text = filename.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                }
            });
            
            // Update results count
            var visibleRows = document.querySelectorAll('.analysis-row[style=""]').length;
            var totalRows = rows.length;
            var resultsInfo = document.getElementById('searchResults');
            if (resultsInfo) {
                resultsInfo.textContent = `Showing ${visibleRows} of ${totalRows} analyses`;
            }
        });
    }
}

// Real-time updates (optional)
function startRealTimeUpdates() {
    // Update dashboard every 30 seconds
    setInterval(function() {
        if (window.location.pathname === '/') {
            updateDashboardStats();
            updateRecentAnalyses();
        }
    }, 30000);
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function() {
    handleFileUpload();
    initializeTableSearch();
    startRealTimeUpdates();
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(function(button) {
        button.addEventListener('click', function(e) {
            var ripple = document.createElement('span');
            var rect = this.getBoundingClientRect();
            var size = Math.max(rect.width, rect.height);
            var x = e.clientX - rect.left - size / 2;
            var y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(function() {
                ripple.remove();
            }, 600);
        });
    });
});

// Add CSS for ripple effect
var style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style); 