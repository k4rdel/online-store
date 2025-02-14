$(document).ready(function() {
  $('.add-to-cart-form').on('submit', function(event) {
      event.preventDefault();
      var form = $(this);
      var url = form.attr('action');
      $.ajax({
          type: 'POST',
          url: url,
          data: form.serialize(),
          success: function(response) {
              var alertBox = $('<div class="alert alert-' + response.category + ' alert-dismissible animate__animated animate__fadeIn" role="alert">' +
                  '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                  '<span aria-hidden="true">&times;</span></button>' + response.message + '</div>');
              $('#alert-container').prepend(alertBox);
              setTimeout(function() {
                  alertBox.addClass('animate__fadeOut');
              }, 3000);
          },
          error: function(response) {
              var alertBox = $('<div class="alert alert-danger alert-dismissible animate__animated animate__fadeIn" role="alert">' +
                  '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                  '<span aria-hidden="true">&times;</span></button>Wystąpił błąd. Spróbuj ponownie.</div>');
              $('#alert-container').prepend(alertBox);
              setTimeout(function() {
                  alertBox.addClass('animate__fadeOut');
              }, 3000);
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const img = document.getElementById("pcPhoto");

  img.addEventListener("click", function () {

    img.classList.add("animate__animated", "animate__tada");

    img.addEventListener("animationend", function () {
      img.classList.remove("animate__animated", "animate__tada");
    }, { once: true });
  });
});

window.setTimeout(function() {
  $(".alert").fadeTo(350, 0) 
}, 4000);