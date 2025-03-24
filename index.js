document.getElementById('imageUpload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        document.getElementById('result').innerText = "Processing image...";

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = `Estimated Age: ${data.estimated_age} years`;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = "Error in processing image.";
        });
    }
});

function estimateAge() {
    document.getElementById('imageUpload').click();
}
