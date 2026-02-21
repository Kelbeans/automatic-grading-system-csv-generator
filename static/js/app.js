// SF10 Grade Automation - Main Application Logic
// Author: Kelvin A. Malabanan

const gradingFiles = [];
let existingSF10 = null;

// DOM Elements
const gradingDropZone = document.getElementById('gradingDropZone');
const gradingFileInput = document.getElementById('gradingFileInput');
const gradingFileList = document.getElementById('gradingFileList');

const sf10DropZone = document.getElementById('sf10DropZone');
const sf10FileInput = document.getElementById('sf10FileInput');
const sf10FileList = document.getElementById('sf10FileList');

const generateBtn = document.getElementById('generateBtn');
const loading = document.getElementById('loading');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');

// Initialize Event Listeners
function init() {
    // Grading sheets events
    gradingDropZone.addEventListener('click', () => gradingFileInput.click());
    gradingDropZone.addEventListener('dragover', handleDragOver);
    gradingDropZone.addEventListener('dragleave', handleDragLeave);
    gradingDropZone.addEventListener('drop', handleGradingDrop);
    gradingFileInput.addEventListener('change', (e) => handleGradingFiles(e.target.files));

    // SF10 events
    sf10DropZone.addEventListener('click', () => sf10FileInput.click());
    sf10DropZone.addEventListener('dragover', handleDragOver);
    sf10DropZone.addEventListener('dragleave', handleDragLeave);
    sf10DropZone.addEventListener('drop', handleSF10Drop);
    sf10FileInput.addEventListener('change', (e) => handleSF10File(e.target.files[0]));

    // Generate button
    generateBtn.addEventListener('click', generateSF10);
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    this.classList.add('dragover');
}

function handleDragLeave() {
    this.classList.remove('dragover');
}

function handleGradingDrop(e) {
    e.preventDefault();
    this.classList.remove('dragover');
    handleGradingFiles(e.dataTransfer.files);
}

function handleSF10Drop(e) {
    e.preventDefault();
    this.classList.remove('dragover');
    handleSF10File(e.dataTransfer.files[0]);
}

// File Handling
function identifyQuarter(filename) {
    const lower = filename.toLowerCase();
    if (lower.includes('1st') || lower.includes('first')) return 1;
    if (lower.includes('2nd') || lower.includes('second')) return 2;
    if (lower.includes('3rd') || lower.includes('third')) return 3;
    if (lower.includes('4th') || lower.includes('fourth')) return 4;
    return null;
}

function handleGradingFiles(files) {
    Array.from(files).forEach(file => {
        const quarter = identifyQuarter(file.name);
        if (quarter) {
            gradingFiles.push({ file, quarter });
        } else {
            alert(`Could not identify quarter from filename: ${file.name}\nPlease include "1st", "2nd", "3rd", or "4th" in the filename.`);
        }
    });
    updateGradingFileList();
    updateGenerateButton();
}

function handleSF10File(file) {
    if (file) {
        existingSF10 = file;
        updateSF10FileList();
    }
}

// UI Updates
function updateGradingFileList() {
    gradingFileList.innerHTML = gradingFiles.map((item, index) => `
        <div class="file-item">
            <div class="file-item-info">
                <div class="file-item-icon">📄</div>
                <div class="file-item-name">${item.file.name}</div>
                <span class="file-item-quarter">Q${item.quarter}</span>
            </div>
            <button class="file-item-remove" onclick="removeGradingFile(${index})">Remove</button>
        </div>
    `).join('');
}

function updateSF10FileList() {
    if (existingSF10) {
        sf10FileList.innerHTML = `
            <div class="file-item">
                <div class="file-item-info">
                    <div class="file-item-icon">📊</div>
                    <div class="file-item-name">${existingSF10.name}</div>
                </div>
                <button class="file-item-remove" onclick="removeSF10File()">Remove</button>
            </div>
        `;
    } else {
        sf10FileList.innerHTML = '';
    }
}

function updateGenerateButton() {
    generateBtn.disabled = gradingFiles.length === 0;
}

// File Removal
function removeGradingFile(index) {
    gradingFiles.splice(index, 1);
    updateGradingFileList();
    updateGenerateButton();
}

function removeSF10File() {
    existingSF10 = null;
    updateSF10FileList();
}

// SF10 Generation
async function generateSF10() {
    const formData = new FormData();

    // Add grading files
    gradingFiles.forEach((item, index) => {
        formData.append(`grading_${index}`, item.file);
    });

    // Add existing SF10 if provided
    if (existingSF10) {
        formData.append('existing_sf10', existingSF10);
    }

    // Hide messages
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';

    // Show loading
    loading.style.display = 'block';
    generateBtn.disabled = true;

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        loading.style.display = 'none';

        if (response.ok) {
            successMessage.innerHTML = `
                <div style="font-size: 16px; font-weight: 600; margin-bottom: 10px;">✅ ${result.message}</div>
                <div style="margin-bottom: 8px;">Quarters processed: ${result.quarters.join(', ')}</div>
                <a href="${result.download_url}" class="download-link">📥 Download SF10 File</a>
            `;
            successMessage.style.display = 'block';

            // Clear files
            gradingFiles.length = 0;
            existingSF10 = null;
            updateGradingFileList();
            updateSF10FileList();
            updateGenerateButton();
        } else {
            errorMessage.textContent = `❌ Error: ${result.error}`;
            errorMessage.style.display = 'block';
            generateBtn.disabled = false;
        }
    } catch (error) {
        loading.style.display = 'none';
        errorMessage.textContent = `❌ Error: ${error.message}`;
        errorMessage.style.display = 'block';
        generateBtn.disabled = false;
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', init);
