const button = document.getElementById("askButton");

button.addEventListener("click", async function () {

    // Get the question from the textbox
    const question = document.getElementById("question").value;

    // Show loading message while AI is processing
    document.getElementById("answer").textContent = "Thinking...";

    // Send question to FastAPI
    const response = await fetch("/ask", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })
    });

    // Convert response to JSON
    const data = await response.json();

    // Replace "Thinking..." with actual answer
    document.getElementById("answer").textContent = data.answer;

});