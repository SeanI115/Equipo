$( document ).ready(function() {
    var formElementsInit = function() {
  // field validations
  $("input:file.validation--failed").parents('input-field').find("input:text.file-path").first().addClass('validation--failed invalid');

  // update labels if there's content
  Materialize.updateTextFields();

  $(".button-collapse").sideNav();
  $('.parallax').parallax();
  $('select').material_select();

  $(".dropdown-button").dropdown({inDuration: 300,
    outDuration: 225,
    constrain_width: false,
    hover: false,
    gutter: 0,
    belowOrigin: true,
    alignment: 'right'
  });
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 100 // Creates a dropdown of 100 years to control year
  });

  $('ul.tabs').tabs();
};


$(document).ready(formElementsInit) //standard jQuery behavior
$(document).on('page:load', formElementsInit) //adaptation to turbolinks
});

