document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("button, .btn-upload-another");
  buttons.forEach((button) => {
    button.addEventListener("mousedown", () => {
      button.style.transform = "scale(0.95)";
    });
    button.addEventListener("mouseup", () => {
      button.style.transform = "scale(1)";
    });
  });
});
