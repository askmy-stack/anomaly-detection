// This code will add a green tickmark to the page with the text below.

function addTickmark() {
    // Get the element that will contain the tickmark.
    var tickmarkElement = document.getElementById("tickmark");

    // Create a new image element and set its source to the tickmark image.
    var imageElement = document.createElement("img");
    imageElement.src = "Green Tick.jpg";

    // Append the image element to the tickmark element.
    tickmarkElement.appendChild(imageElement);
}

// Add the tickmark to the page when the page loads.
window.onload = addTickmark;
