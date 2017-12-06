
var Tracker = (function() {
        $(document).ready(function() {
          $('select').material_select();
        });

        var id;
        var role;

        var populateProf = function(){
          url = 'ProfByID/'
          id = getParameterByName('id')
          var onSuccess = function(data){
            $('#first_name').val(data.prof.firstName)
            $('#last_name').val(data.prof.lastName)
            $('#email').val(data.prof.email)
            $('#ID').val(data.prof.id)
          }
          var onError = function(data){
          }
          makeGetRequest(url+id, onSuccess, onError)
        }

        var getParameterByName = function(name, url) {
            if (!url) url = window.location.href;
            name = name.replace(/[\[\]]/g, "\\$&");
            var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, " "));
        }

        var start = function() {
            id = getParameterByName('id')
            role = getParameterByName('role')
            populateProf()
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
var apiUrl = 'http://127.0.0.1:5000/api/';
var CREATE_COURSE_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfCourseCreate.html"
var MY_CLASSES_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfSplash.html"
var MANAGE_TAS_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfTAPicker.html"

var makeGetRequest = function(url, onSuccess, onFailure) {
    $.ajax({
        type: 'GET',
        url: apiUrl + url,
        dataType: "json",
        success: onSuccess,
        error: onFailure
    });
};

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

function TAPickerRedirect(){
    var url= window.location.href;
    var splitIndex = url.indexOf("?");
    var info = '';
    if(splitIndex !=-1){
      info = url.slice(splitIndex);
    }
    var newUrl = MANAGE_TAS_REDIRECT_URL + info;
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

function editInfo(){
  var data = {}

  data.firstName = document.getElementById('first_name').value;
  data.lastName = document.getElementById('last_name').value;
  data.id= document.getElementById('ID').value;

  var onSuccess = function(e){
    alert('Yay')
  }

  var onError = function(e){
    alert('awww')
  }

  makePostRequest('editProf', data, onSuccess, onError)
}

var getParameterByNamePub = function(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function showStuff(box){
  if(box.checked) $('.dayTime').show();
  else $('.dayTime').hide();
}


var apiUrl = 'http://127.0.0.1:5000/api/';
