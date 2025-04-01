function generateDescription(productId) {
    // Ensure that the productId is an integer
    console.log("Product ID: " + productId);  // Check the ID output
    fetch(`/generate_description/${productId}`)
    .then(response => response.json())
    .then(data => {
        alert('Generated Description: ' + data.description);
        document.getElementById('wordcloud-image').src = data.wordcloud;
    })
    .catch(error => console.log(error));
}
