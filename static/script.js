document.getElementById('uploadButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const output = document.getElementById('output');

    if (fileInput.files.length === 0) {
        alert('Please select a .fidscy file');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/interpret', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        output.textContent = data;
    })
    .catch(error => {
        console.error('Error:', error);
        output.textContent = 'An error occurred while interpreting the file.';
    });
});
