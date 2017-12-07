
var Tracker = (function() {
        $(document).ready(function() {
          $('select').material_select();
        });

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

        var start = function() {
            id = getParameterByName('id')
            role = getParameterByName('role')
            $('.dayTime').hide();
            $('#repeatMessage').hide();
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
var apiUrl = 'http://127.0.0.1:5000/api/';
var MY_INFO_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfInfo.html"
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
var LOG_OUT_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/login.html"
function logoutRedirect(){
  window.location.href = LOG_OUT_REDIRECT_URL
}

function attemptCourseCreate(){
  var data = {}

  data.userID=getParameterByNamePub('id')
  data.role=getParameterByNamePub('role')
  data.professorID=getParameterByNamePub('id')
  data.prefix=document.getElementById('classPrefix').value;
  data.courseNumber=document.getElementById('classNum').value;
  data.semester=document.getElementById('semester').value;
  data.section=document.getElementById('section').value;
  data.numTAsNeeded=document.getElementById('numTAsNeeded').value;
  data.numTAsAdded=0;
  data.labSection=document.getElementById('section').value;
  data.dayTime = '';
  var b = document.getElementById('dayTime').checked
  if(b){
    data.dayTime=document.getElementById('dayTimeIn').value;
  }

  var onSuccess = function(e){
    $("#repeatMessage").show()
  }

  var onError = function(e){
    alert('awww')
  }

  makePostRequest('createClass', data, onSuccess, onError)
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
