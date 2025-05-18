/**
 * Encryption App Module
 * 
 * Structured following OOP and SOLID principles
 */

// Global functions for direct HTML access
function switchTab(tabName) {
    app.tabs.switchTab(tabName);
}

function switchInputMethod(method) {
    app.inputMethods.switchMethod(method);
}

function handleFileUpload(input) {
    app.fileUploader.updateFileLabel(input);
}

function downloadEncryptedData() {
    app.resultManager.downloadEncryptedData();
}

function resetAll() {
    app.resetManager.resetAllData();
}

// UI Components
class TabManager {
    constructor() {
        this.tabs = document.querySelectorAll('.tab');
        this.tabContents = document.querySelectorAll('.tab-content');
    }

    switchTab(tabName) {
        this.tabs.forEach(tab => tab.classList.remove('active'));
        this.tabContents.forEach(tab => tab.classList.remove('active'));
        
        document.getElementById(tabName + '-tab').classList.add('active');
        document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`).classList.add('active');
    }
}

class InputMethodManager {
    constructor() {
        this.methods = document.querySelectorAll('.input-method');
        this.fileUpload = document.getElementById('file-upload');
        this.textUpload = document.getElementById('text-upload');
        this.fileInput = document.getElementById('encrypted-file');
        this.textInput = document.getElementById('encrypted-json');
    }

    switchMethod(method) {
        // Update selection styling
        this.methods.forEach(el => el.classList.remove('active'));
        document.querySelector(`.input-method[onclick="switchInputMethod('${method}')"]`).classList.add('active');
        
        if (method === 'file') {
            this.fileUpload.classList.add('active');
            this.textUpload.classList.remove('active');
            this.textInput.value = '';
        } else {
            this.fileUpload.classList.remove('active');
            this.textUpload.classList.add('active');
            this.fileInput.value = '';
            this.resetFileLabel();
        }
    }

    resetFileLabel() {
        const label = this.fileUpload.querySelector('label span');
        if (label) {
            label.textContent = 'Click to select file or drag and drop';
        }
    }
}

class FileUploader {
    constructor() {
        this.dropArea = document.querySelector('.file-upload');
        this.fileInput = document.getElementById('encrypted-file');
        this.initDragAndDrop();
    }

    initDragAndDrop() {
        if (!this.dropArea) return;
        
        // Prevent default behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
            this.dropArea.addEventListener(event, e => {
                e.preventDefault();
                e.stopPropagation();
            });
        });
        
        // Highlight when dragging over
        ['dragenter', 'dragover'].forEach(event => {
            this.dropArea.addEventListener(event, () => {
                this.dropArea.classList.add('highlight');
            });
        });
        
        // Remove highlight
        ['dragleave', 'drop'].forEach(event => {
            this.dropArea.addEventListener(event, () => {
                this.dropArea.classList.remove('highlight');
            });
        });
        
        // Handle file drop
        this.dropArea.addEventListener('drop', e => this.handleDrop(e));
    }
    
    handleDrop(e) {
        if (!e.dataTransfer || !e.dataTransfer.files) return;
        
        this.fileInput.files = e.dataTransfer.files;
        this.updateFileLabel();
    }
    
    updateFileLabel(input = null) {
        const fileInput = input || this.fileInput;
        if (fileInput.files && fileInput.files[0]) {
            const fileName = fileInput.files[0].name;
            const label = this.dropArea.querySelector('label span');
            if (label) {
                label.textContent = `Selected: ${fileName}`;
            }
        }
    }
}

class ResultManager {
    constructor() {
        // This class will initialize only when needed
    }
    
    downloadEncryptedData() {
        const resultElement = document.querySelector('.result textarea');
        if (!resultElement) return;
        
        const encryptedData = resultElement.value;
        const dataBlob = new Blob([encryptedData], {type: 'application/json'});
        const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
        
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(dataBlob);
        downloadLink.download = `encrypted_${timestamp}.json`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }
}

class ResetManager {
    constructor() {
        // This class handles resetting all forms and data
    }
    
    resetAllData() {
        // Clear all forms
        document.querySelectorAll('form').forEach(form => form.reset());
        
        // Clear file input
        const fileInput = document.getElementById('encrypted-file');
        if (fileInput) fileInput.value = '';
        
        // Reset file upload label
        const fileLabel = document.querySelector('.file-upload label span');
        if (fileLabel) fileLabel.textContent = 'Click to select file or drag and drop';
        
        // Clear text areas
        document.querySelectorAll('textarea').forEach(textarea => {
            if (!textarea.readOnly) {
                textarea.value = '';
            }
        });
        
        // Remove result sections
        document.querySelectorAll('.result').forEach(result => {
            result.remove();
        });
        
        // Remove alerts
        document.querySelectorAll('.alert').forEach(alert => {
            alert.remove();
        });
        
        // Switch to encrypt tab
        const tabManager = new TabManager();
        tabManager.switchTab('encrypt');
        
        // Reset input method to file
        const inputMethodManager = new InputMethodManager();
        inputMethodManager.switchMethod('file');
        
        console.log('All data has been reset');
        
        // Send a POST request to the server to reset data
        fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        })
        .then(response => {
            if (response.ok) {
                // Use hard navigation instead of just reloading
                window.location.href = '/?reset=true&nocache=' + new Date().getTime();
            }
        })
        .catch(error => {
            console.error('Error resetting data:', error);
        });
    }
}

// Main App
class EncryptionApp {
    constructor() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initComponents();
            this.initialize();
        });
    }
    
    initComponents() {
        this.tabs = new TabManager();
        this.inputMethods = new InputMethodManager();
        this.fileUploader = new FileUploader();
        this.resultManager = new ResultManager();
        this.resetManager = new ResetManager();
    }
    
    initialize() {
        const pageData = document.getElementById('page-data');
        if (pageData && pageData.getAttribute('data-should-switch-decrypt') === 'true') {
            this.tabs.switchTab('decrypt');
        }
    }
}

// Initialize the app
const app = new EncryptionApp(); 