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
                var alertBox = $('<div class="alert alert-' + response.category + ' alert-dismissible animate__animated animate__fadeInDown" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span></button>' + response.message + '</div>');
                $('#alert-container').prepend(alertBox);
                setTimeout(function() {
                    alertBox.addClass('animate__fadeOutUp');
                    alertBox.one('animationend', function() {
                        $(this).remove();
                    });
                }, 3000);

                var product = response.product;
                var cartItem = $('#cart-item-' + product.id);
                if (cartItem.length) {
                    cartItem.find('.quantity').text('Ilość: ' + product.quantity);
                } else {
                    var newItem = $('<li id="cart-item-' + product.id + '">' +
                        'Produkt: ' + product.name + '<br>' +
                        '<span class="quantity">Ilość: ' + product.quantity + '</span><br>' +
                        'Cena: ' + product.price + ' PLN<br>' +
                        '<button class="btn btn-danger" onclick="removeFromCart(' + product.id + ')">Remove</button>' +
                        '</li>');
                    $('#cartModal .modal-body ul').append(newItem);
                }
                $('#cart-count').text(response.total_items);
            },
            error: function(response) {
                var alertBox = $('<div class="alert alert-danger alert-dismissible animate__animated animate__fadeInDown" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span></button>Wystąpił błąd. Spróbuj ponownie.</div>');
                $('#alert-container').prepend(alertBox);
                setTimeout(function() {
                    alertBox.addClass('animate__fadeOutUp');
                    alertBox.one('animationend', function() {
                        $(this).remove();
                    });
                }, 3000);
            }
        });
    });
});

function removeFromCart(itemId) {
    $.ajax({
        type: 'POST',
        url: '/remove_from_cart/' + itemId,
        success: function(response) {
            var alertBox = $('<div class="alert alert-' + response.category + ' alert-dismissible animate__animated animate__fadeInDown" role="alert">' +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                '<span aria-hidden="true">&times;</span></button>' + response.message + '</div>');
            $('#alert-container').prepend(alertBox);
            setTimeout(function() {
                alertBox.addClass('animate__fadeOutUp');
                alertBox.one('animationend', function() {
                    $(this).remove();
                });
            }, 3000);
            $('#cart-item-' + itemId).remove();
        },
        error: function(response) {
            var alertBox = $('<div class="alert alert-danger alert-dismissible animate__animated animate__fadeInDown" role="alert">' +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                '<span aria-hidden="true">&times;</span></button>Wystąpił błąd. Spróbuj ponownie.</div>');
            $('#alert-container').prepend(alertBox);
            setTimeout(function() {
                alertBox.addClass('animate__fadeOutUp');
                alertBox.one('animationend', function() {
                    $(this).remove();
                });
            }, 3000);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const img = document.getElementById("pcPhoto");

  img.addEventListener("click", function () {

    img.classList.add("animate__animated", "animate__tada");

    img.addEventListener("animationend", function () {
      img.classList.remove("animate__animated", "animate__tada");
    }, { once: true });
  });
});

document.querySelectorAll('.product').forEach(function(div) {
  div.addEventListener('click', function() {
    window.location.href = div.getAttribute('data-url');
  });
});

