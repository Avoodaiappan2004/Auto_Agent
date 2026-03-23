async function runAgent() {
    const task = document.getElementById("taskInput").value;

    if (!task) {
        alert("Enter a task!");
        return;
    }

    document.getElementById("status").innerText = "Running...";
    document.getElementById("logs").innerText = "";
    document.getElementById("githubLink").innerHTML = "";

    try {
        const res = await fetch("https://auto-agent-54cl.onrender.com/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ task })
        });

        const data = await res.json();

        // ✅ STATUS
        document.getElementById("status").innerText = data.status;

        // ✅ GITHUB LINK (only if exists)
        if (data.github && data.github !== "") {
            document.getElementById("githubLink").innerHTML =
                `🔗 <a href="${data.github}" target="_blank">View GitHub Repo</a>`;
        }

        // ✅ LOGS (direct from backend)
        if (data.logs) {
            document.getElementById("logs").innerText =
                JSON.stringify(data.logs, null, 2);
        } else {
            document.getElementById("logs").innerText = "No logs found";
        }

    } catch (err) {
        console.error(err);
        document.getElementById("status").innerText = "Error connecting backend";
    }
    window.addEventListener("beforeunload", function () {
    console.log("Page is reloading...");
});
}