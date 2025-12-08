const rootUrl = "http://localhost:8080";

const endpoint = rootUrl + "/health";
const res = await fetch(endpoint, {
    method: "GET",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({})
});
resJson = await res.json();
console.log(resJson['status'])