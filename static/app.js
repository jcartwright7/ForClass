const questionBox = document.getElementById("question");
const askButton = document.getElementById("askButton");
const answerBox = document.getElementById("answer");
const statusBox = document.getElementById("status");

askButton.addEventListener("click", async () => {
    const text = questionBox.value.trim();

    if (!text) {
        statusBox.textContent = "Please type a question first.";
        return;
    }

    askButton.disabled = true;
    statusBox.textContent = "Thinking...";
    answerBox.textContent = "";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        answerBox.textContent = data.answer;
        statusBox.textContent = "Done.";
    } catch (error) {
        answerBox.textContent = "";
        statusBox.textContent = error.message;
    } finally {
        askButton.disabled = false;
    }
});
