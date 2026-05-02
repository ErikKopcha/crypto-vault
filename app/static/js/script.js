// UI Components
class TabManager {
  constructor() {
    this.tabs = document.querySelectorAll('.tab');
    this.tabContents = document.querySelectorAll('.tab-content');
    this.tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        if (tabName) this.switchTab(tabName);
      });
    });
  }

  switchTab(tabName) {
    this.tabs.forEach((tab) => tab.classList.remove('active'));
    this.tabContents.forEach((tab) => tab.classList.remove('active'));

    document.getElementById(tabName + '-tab').classList.add('active');
    document
      .querySelector(`.tab[data-tab="${tabName}"]`)
      .classList.add('active');
  }
}

class InputMethodManager {
  constructor() {
    this.methods = document.querySelectorAll('.input-method');
    this.fileUpload = document.getElementById('file-upload');
    this.textUpload = document.getElementById('text-upload');
    this.fileInput = document.getElementById('encrypted-file');
    this.textInput = document.getElementById('encrypted-json');
    this.methods.forEach((methodElement) => {
      methodElement.addEventListener('click', () => {
        const method = methodElement.dataset.method;
        if (method) this.switchMethod(method);
      });
    });
  }

  switchMethod(method) {
    this.methods.forEach((el) => el.classList.remove('active'));
    document
      .querySelector(`.input-method[data-method="${method}"]`)
      .classList.add('active');

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
    this.fileInput?.addEventListener('change', () => {
      this.updateFileLabel(this.fileInput);
    });
  }

  initDragAndDrop() {
    if (!this.dropArea) return;

    // Prevent default behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((event) => {
      this.dropArea.addEventListener(event, (e) => {
        e.preventDefault();
        e.stopPropagation();
      });
    });

    // Highlight when dragging over
    ['dragenter', 'dragover'].forEach((event) => {
      this.dropArea.addEventListener(event, () => {
        this.dropArea.classList.add('highlight');
      });
    });

    // Remove highlight
    ['dragleave', 'drop'].forEach((event) => {
      this.dropArea.addEventListener(event, () => {
        this.dropArea.classList.remove('highlight');
      });
    });

    // Handle file drop
    this.dropArea.addEventListener('drop', (e) => this.handleDrop(e));
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
    document
      .getElementById('download-btn')
      ?.addEventListener('click', () => this.downloadEncryptedData());
  }

  downloadEncryptedData() {
    const resultElement = document.querySelector('.result textarea');
    if (!resultElement) return;

    const encryptedData = resultElement.value;
    const dataBlob = new Blob([encryptedData], { type: 'application/json' });
    const timestamp = new Date()
      .toISOString()
      .replace(/:/g, '-')
      .replace(/\..+/, '');

    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(dataBlob);
    downloadLink.download = `encrypted_${timestamp}.json`;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
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
  }

  initialize() {
    const pageData = document.getElementById('page-data');

    if (
      pageData &&
      pageData.getAttribute('data-should-switch-decrypt') === 'true'
    ) {
      this.tabs.switchTab('decrypt');
    }
  }
}

const app = new EncryptionApp();
