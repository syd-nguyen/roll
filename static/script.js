const newBoardForm = document.getElementById("newBoardForm");
const eventName = document.getElementById("eventName");

newBoardForm.addEventListener("submit", async (e) => {

    e.preventDefault();
    const text = eventName.value.trim();
    if (!text) return;
        
    try {
        const endpoint = "http://127.0.0.1:5000/api/echo";
        const res = await fetch(endpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text })
        });

        const toprint = await res.json();
        console.log(toprint);
    } catch (err) {
        console.log("error");
    }

});