document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const form = new FormData(this);
    
    const res = await fetch("/upload/document", {
        method: "POST",
        body: form
    });
    
    const data = await res.json();
    document.getElementById("response").textContent = JSON.stringify(data, null, 2);
});
