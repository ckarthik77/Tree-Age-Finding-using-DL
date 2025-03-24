document.getElementById('imageUpload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('result').innerText = "Processing image...";
            // Simulate Deep Learning model processing
            setTimeout(() => {
                const estimatedAge = Math.floor(Math.random() * 100) + 1; // Placeholder logic
                document.getElementById('result').innerText = `Estimated Age: ${estimatedAge} years`;
            }, 2000);
        };
        reader.readAsDataURL(file);
    }
});

function estimateAge() {
    document.getElementById('imageUpload').click();
}
