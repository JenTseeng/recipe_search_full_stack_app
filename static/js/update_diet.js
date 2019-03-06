"use strict";

function updateDiet() {
  $('#diet-update-form').on('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
      'diet': $('input[name=diet]:checked').val(),
      'health': $('input[name=health]:checked').val(),
    };
    console.log(formInputs);


    $.post('/update_diet', formInputs, (results) => {
      alert(results);
    });
  });
}


function updateIngredients() {
  $('#ingredient-form').on('submit', (evt) => {
    evt.preventDefault();
    const formInput = {
      'ingredient-text': $('#ingredient-text-box').val(),
    };
    console.log(formInput);


    $.post('/update_ingred_preferences', formInput, (results) => {
      alert(results);
    });
  });
}



updateIngredients();
updateDiet();