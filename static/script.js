const newBoardForm = document.getElementById("newBoardForm");
const eventNameField = document.getElementById("eventNameField");

newBoardForm.addEventListener("submit", async (e) => {

    e.preventDefault();
    const eventName = eventNameField.value.trim();
    if (!eventName) return;
        
    try {
        const endpoint = "http://127.0.0.1:5000/api/send-event-to-mongo";
        const res = await fetch(endpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ eventName })
        });

    } catch (err) {
        console.log("error");
    }

});