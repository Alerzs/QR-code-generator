const form = document.querySelector('form')
const input = document.querySelector('form input')
const qrImg = document.getElementById("QR")

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    const data = input.value.trim();
    if (!data) {
    alert("Please enter text or URL");
    return;
    }
    try {
    const response = await fetch("http://127.0.0.1:8000/qr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: data })
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    qrImg.src = url;
    } catch (err) {
    console.error(err);
    alert("Error generating QR code");
    }
});