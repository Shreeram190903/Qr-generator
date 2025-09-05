/*
QR Generator Pro - JavaScript Functions (TEMPLATE SYNTAX FIXED)
Created by: Shreeram
Copyright © 2024 Shreeram. All rights reserved.
*/

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 QR Generator Pro by Shreeram - TEMPLATE SYNTAX FIXED VERSION Loaded!');
    console.log('© 2024 Shreeram. All rights reserved.');

    // Initialize tooltips
    try {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    } catch (e) {
        console.warn('Tooltips failed to initialize:', e);
    }

    // Add fade-in animation to main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.classList.add('fade-in-up');
    }

    // Update range slider values
    const boxSizeSlider = document.getElementById('box_size');
    const borderSlider = document.getElementById('border');
    const boxSizeValue = document.getElementById('box_size_value');
    const borderValue = document.getElementById('border_value');

    if (boxSizeSlider && boxSizeValue) {
        boxSizeSlider.addEventListener('input', function() {
            boxSizeValue.textContent = this.value;
        });
    }

    if (borderSlider && borderValue) {
        borderSlider.addEventListener('input', function() {
            borderValue.textContent = this.value;
        });
    }

    // Handle form submission with proper error handling
    const qrForm = document.getElementById('qrForm');
    if (qrForm) {
        qrForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('🚀 QR Generation started by Shreeram');
            generateQRCode();
        });
    }

    // Real-time URL validation
    const urlInput = document.getElementById('url');
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const value = this.value.trim();

            if (value && value.length > 0) {
                // Basic URL validation - more lenient
                const hasProtocol = value.startsWith('http://') || value.startsWith('https://');
                const hasDomain = value.includes('.') && value.length > 3;

                if (!hasProtocol && !hasDomain) {
                    this.setCustomValidity('Please enter a valid URL (e.g., https://example.com or example.com)');
                } else {
                    this.setCustomValidity('');
                }
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Enhanced color picker interactions
    const colorPickers = document.querySelectorAll('input[type="color"]');
    colorPickers.forEach(picker => {
        const preview = document.createElement('div');
        preview.className = 'color-preview mt-2';
        preview.style.cssText = 'width: 100%; height: 20px; border-radius: 5px; border: 1px solid #ddd; background: ' + picker.value + '; transition: background 0.3s ease;';

        if (picker.parentNode) {
            picker.parentNode.appendChild(preview);
        }

        picker.addEventListener('input', function() {
            preview.style.background = this.value;
        });
    });
});

// MAIN FUNCTION: Generate QR Code - CORRECTED VERSION
function generateQRCode() {
    console.log('🎨 generateQRCode() called - Shreeram\'s algorithm starting...');

    const form = document.getElementById('qrForm');
    const generateBtn = document.getElementById('generateBtn');
    const loadingDiv = document.getElementById('loading');
    const placeholderDiv = document.getElementById('placeholder');
    const previewArea = document.getElementById('preview-area');

    if (!form) {
        console.error('❌ Form not found!');
        showAlert('Form not found - please refresh the page', 'error');
        return;
    }

    // Validate form first
    if (!form.checkValidity()) {
        console.log('❌ Form validation failed');
        form.reportValidity();
        return;
    }

    // Get form data
    const formData = new FormData(form);

    // Debug form data
    console.log('📋 Form data being sent:');
    for (let [key, value] of formData.entries()) {
        console.log('   ' + key + ': ' + value);
    }

    // Show loading state
    if (generateBtn) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating by Shreeram...';
    }

    if (loadingDiv) {
        loadingDiv.classList.remove('d-none');
    }

    if (placeholderDiv) {
        placeholderDiv.classList.add('d-none');
    }

    if (previewArea) {
        previewArea.classList.add('d-none');
    }

    console.log('🌐 Sending request to /generate...');

    // Make the request with enhanced error handling
    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('📨 Response received:', response.status, response.statusText);

        if (!response.ok) {
            throw new Error('HTTP ' + response.status + ': ' + response.statusText);
        }

        return response.json();
    })
    .then(data => {
        console.log('📊 Response data:', data);

        if (data.success) {
            console.log('✅ QR code generated successfully!');

            // Show preview
            const qrPreview = document.getElementById('qr-preview');
            const downloadBtn = document.getElementById('downloadBtn');

            if (qrPreview && data.preview_url) {
                qrPreview.src = data.preview_url + '?t=' + Date.now();
                qrPreview.alt = '';
                console.log('🖼️ Preview image set:', qrPreview.src);
            }

            if (downloadBtn && data.download_url) {
                downloadBtn.onclick = function() {
                    console.log('📥 Download initiated');
                    window.open(data.download_url, '_blank');
                };
            }

            if (previewArea) {
                previewArea.classList.remove('d-none');
            }

            // Show success alert
            showAlert(data.message || 'QR code generated successfully by Shreeram!', 'success');
        } else {
            console.error('❌ Server returned error:', data.error);
            showAlert(data.error || 'Failed to generate QR code', 'error');
            if (placeholderDiv) {
                placeholderDiv.classList.remove('d-none');
            }
        }
    })
    .catch(error => {
        console.error('❌ Network or parsing error:', error);
        showAlert('Network error: ' + error.message + ' - Please check your connection and try again.', 'error');
        if (placeholderDiv) {
            placeholderDiv.classList.remove('d-none');
        }
    })
    .finally(() => {
        console.log('🔄 Request completed, resetting UI...');

        // Reset button state
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="bi bi-magic me-2"></i>Generate QR Code';
        }

        if (loadingDiv) {
            loadingDiv.classList.add('d-none');
        }
    });
}

function generateNew() {
    console.log('🔄 Generating new QR code...');
    const previewArea = document.getElementById('preview-area');
    const placeholder = document.getElementById('placeholder');

    if (previewArea) {
        previewArea.classList.add('d-none');
    }

    if (placeholder) {
        placeholder.classList.remove('d-none');
    }
}

// Better alert function
function showAlert(message, type) {
    console.log('🔔 Showing ' + type + ' alert:', message);

    let alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.id = 'alertContainer';
        alertContainer.className = 'position-fixed top-0 end-0 p-3';
        alertContainer.style.zIndex = '1080';
        document.body.appendChild(alertContainer);
    }

    const alertType = type === 'success' ? 'alert-success' : 'alert-danger';
    const icon = type === 'success' ? 'check-circle-fill' : 'exclamation-triangle-fill';
    const alertId = 'alert-' + Date.now();

    const alertHtml = '<div id="' + alertId + '" class="alert ' + alertType + ' alert-dismissible fade show" role="alert">' +
        '<i class="bi bi-' + icon + ' me-2"></i>' + message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
        '</div>';

    alertContainer.insertAdjacentHTML('beforeend', alertHtml);

    // Auto-dismiss
    const dismissTime = type === 'error' ? 10000 : 5000;
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            alertElement.remove();
        }
    }, dismissTime);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        const qrForm = document.getElementById('qrForm');
        if (qrForm && qrForm.checkValidity()) {
            generateQRCode();
        }
    }

    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        if (modals.length === 0) {
            generateNew();
        }
    }
});

// Debug function
function testBackend() {
    console.log('🧪 Testing backend connection...');
    fetch('/test')
        .then(response => response.json())
        .then(data => {
            console.log('✅ Backend test successful:', data);
            showAlert('Backend is working: ' + data.message, 'success');
        })
        .catch(error => {
            console.error('❌ Backend test failed:', error);
            showAlert('Backend test failed: ' + error.message, 'error');
        });
}

// Export functions for debugging
window.QRGeneratorByShreeram = {
    generateQRCode: generateQRCode,
    generateNew: generateNew,
    showAlert: showAlert,
    testBackend: testBackend,
    version: '1.0.2-TEMPLATE-SYNTAX-FIXED',
    author: 'Shreeram',
    copyright: '© 2024 Shreeram. All rights reserved.'
};

console.log('🚀 QR Generator Pro v1.0.2-TEMPLATE-SYNTAX-FIXED');
console.log('👨‍💻 Created by: Shreeram');  
console.log('© 2024 Shreeram. All rights reserved.');
console.log('🔧 All template syntax issues fixed!');
console.log('🎯 Ready for production deployment!');
