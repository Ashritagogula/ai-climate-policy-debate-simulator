async function startDebate() {
    const topic = document.getElementById("topic").value;
    const rounds = parseInt(document.getElementById("rounds").value);

    const response = await fetch("/debate/start", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            topic,
            rounds
        })
    });

    const data = await response.json();

    document.getElementById("output").textContent =
        JSON.stringify(data, null, 2);
}