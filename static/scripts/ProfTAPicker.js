var Tracker = (function() {

  var start = function() {
      id = getParameterByName('id');
      role = getParameterByName('role');
      classID = getParameterByName('classID');

      displayTAs();

  };

  // PUBLIC METHODS
  // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start(
  return {
      start: start
    };


  })();

  var PROF_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfSplash.html"
  var apiUrl = 'http://127.0.0.1:5000/api/';

 /**
  * HTTP GET request
  * @param  {string}   url       URL path, e.g. "/api/smiles"
  * @param  {function} onSuccess   callback method to execute upon request success (200 status)
  * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
  * @return {None}
  */
 var makeGetRequest = function(url, onSuccess, onFailure) {
     $.ajax({
         type: 'GET',
         url: apiUrl + url,
         dataType: "json",
         success: onSuccess,
         error: onFailure
     });
 };
  /**
   * HTTP POST request
   * @param  {string}   url       URL path, e.g. "/api/smiles"
   * @param  {Object}   data      JSON data to send in request body
   * @param  {function} onSuccess   callback method to execute upon request success (200 status)
   * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
   * @return {None}
   */
  var makePostRequest = function(url, data, onSuccess, onFailure) {
      $.ajax({
          type: 'POST',
          url: apiUrl + url,
          data: JSON.stringify(data),
          contentType: "application/json",
          dataType: "json",
          success: onSuccess,
          error: onFailure
      });
  };

  var submitAppSelections = function() {

    var onSuccess = {

    };
    var onFailure = {

    };

    var selected = [];
    $('input:checked').each(function() {
      selected.push($(this).attr('id'));
    });

    for(var i = 0; i < selected.length; i++){

        var chosen = {};
        chosen.id = selected[i];
        makePostRequest('addTA',chosen,onSuccess,onFailure)
    }

    var redirectUrl = PROF_REDIRECT_URL;
    redirectUrl += '?id=' + id +'&role=' + role;
    window.location.replace(redirectUrl);
  };


  var displayTAs = function() {

    var onSuccess = function(data) {

        var form = $(".TAselect");
        var $input = $('<input type="text">').attr({id: 'from', name: 'from'});

        var appID = '';
        var TAName = '';
        var TAMajor = '';
        var gradeInClass = '';
        var story = '';

        for(var i = 0; i < data.apps.length; i++){

              appID = data.apps[i].id;
              TAName = data.apps[i].TAFirstName + ' ' + data.apps[i].TALastName;
              TAMajor = data.apps[i].TAmajor;
              gradeInClass = data.apps[i].gradeInClass;
              story = data.apps[i].story;

              var TAProfiles = $('<div />').attr({class: 'collection'});

              $("<label>").text(TAName).attr({class: 'collection-item'}).appendTo(TAProfiles);
              $("<label>").text(TAMajor).attr({class: 'collection-item'}).appendTo(TAProfiles);
              $("<label>").text(gradeInClass).attr({class: 'collection-item'}).appendTo(TAProfiles);
              $("<label>").text(story).attr({class: 'collection-item'}).appendTo(TAProfiles);

              $('<input type="checkbox" class="checkboxes">').attr({id: appID, class: 'collection.item'}).appendTo(TAProfiles);

              TAProfiles.appendTo(form);
        }

      };
    var onFailure = function() {

      };

    makeGetRequest('AppsForClass/'+classID+'/',onSuccess,onFailure);

  };


  var displayClass = function() {

    var onSuccess = function(data) {

        var section = $(".classDrop");
        var classDrop = $('<select />');
        var classBoxes = $('<div />');
        var className = '';
        var $input = $('<input type="text">').attr({id: 'from', name: 'from'});

        for(var i = 0; i < data.classes.length; i++){

              className = data.classes[i].prefix + '-' + data.classes[i].courseNumber;

              $('<option />', {value: className, text: className}).appendTo(classDrop);
              $("<label>").text(className).appendTo(classBoxes);
              $('<input type="checkbox">').appendTo(classBoxes);

          }

        classDrop.appendTo(section); // or wherever it should be
        classBoxes.appendTo(section);
      };
    var onFailure = function() {


      };

    makeGetRequest('ClassesByProfID/'+id+'/'+role+'/', onSuccess, onFailure);

  };

  var MY_INFO_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfInfo.html"
  var MY_CLASSES_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfSplash.html"
  var CREATE_COURSE_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfTAPicker.html"


  function myClassesRedirect(){
    var url= window.location.href;
    var splitIndex = url.indexOf("?");
    var info = '';
    if(splitIndex !=-1){
      info = url.slice(splitIndex);
    }
    var newUrl = MY_CLASSES_REDIRECT_URL + info;
    window.location.href = newUrl;

  }

  function createCourseRedirect(){
      var url= window.location.href;
      var splitIndex = url.indexOf("?");
      var info = '';
      if(splitIndex !=-1){
        info = url.slice(splitIndex);
      }
      var newUrl = CREATE_COURSE_REDIRECT_URL + info;
      window.location.href = newUrl;
  }

  function myInfoRedirect(){
    var url= window.location.href;
    var splitIndex = url.indexOf("?");
    var info = '';
    if(splitIndex !=-1){
      info = url.slice(splitIndex);
    }
    var newUrl = MY_INFO_REDIRECT_URL + info;
    window.location.href = newUrl;
  }

  var id;
  var role;

  var getParameterByName = function(name, url) {
      if (!url) url = window.location.href;
      name = name.replace(/[\[\]]/g, "\\$&");
      var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
          results = regex.exec(url);
      if (!results) return null;
      if (!results[2]) return '';
      return decodeURIComponent(results[2].replace(/\+/g, " "));
    }
