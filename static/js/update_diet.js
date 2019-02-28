"use strict";

function updateDiet() {
  $('#diet-update-form').on('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
      'diet': $('#diet-field').val(),
      'health': $('#health-field').val()
    };

    $.post('/update_diet', formInputs, (results) => {
      alert(results);
    });
  });
}

updateDiet();