document.addEventListener("DOMContentLoaded", function () {
    const img = document.getElementById("pcPhoto");
  
    img.addEventListener("click", function () {

      img.classList.add("animate__animated", "animate__tada");
  
      img.addEventListener("animationend", function () {
        img.classList.remove("animate__animated", "animate__tada");
      }, { once: true });
    });
  });