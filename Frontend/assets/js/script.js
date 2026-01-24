console.log("script.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("year").textContent = new Date().getFullYear();

  fetch("https://resume-visitor-api.azurewebsites.net/api/visitcounter")
    .then(response => response.json())
    .then(data => {
      document.getElementById("counter").textContent = data.count;
    })
    .catch(err => console.error("Visitor counter error:", err));
});
