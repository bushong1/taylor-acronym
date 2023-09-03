
// Function to search for acronyms
function searchAcronym() {
    // Get the entered acronym from the input field
    const acronym = document.getElementById("acronymInput").value.trim().toUpperCase();

    // Validate the entered acronym
    if (acronym.length < 4 || acronym.length > 20) {
        alert("Please enter an acronym between 4 and 20 characters long, inclusive.");
        return;
    }

    // Determine the appropriate JSON file based on acronym length
    const jsonFile = "acronyms/acronym_" + acronym.length + ".json";

    // Fetch the JSON file and search for the acronym
    fetch(jsonFile)
        .then(response => response.json())
        .then(data => {
            // Get the matches for the entered acronym
            const matches = data[acronym] || [];

            // Populate the results table with the matches
            const tableBody = document.querySelector("#resultsTable tbody");
            tableBody.innerHTML = "";
            for (const match of matches) {
                const row = tableBody.insertRow();
                row.insertCell().textContent = match[0]; // Song title
                row.insertCell().textContent = match[1]; // Matching lyric
            }
        })
        .catch(error => {
            console.error("Error fetching or processing the JSON file:", error);
            alert("An error occurred while processing your request. Please try again later.");
        });
}
