var Tracker = (function() {
        $(document).ready(function() {
          $('select').material_select();
        });

        var id;
        var role;

        var populateTA = function(){
          url = 'TAByID/'
          id = getParameterByName('id')
          var onSuccess = function(data){
            $('#first_name').val(data.ta.firstName)
            $('#last_name').val(data.ta.lastName)
            $('#email').val(data.ta.email)
            $('#ID').val(data.ta.id)
						$('#major').val(data.ta.major)
            $('#cum_gpa').val(data.ta.cum_gpa)
            $('#expected_grad').val(data.ta.expected_grad)
            $('#prev_Ta').val(data.ta.prev_TA)
						$('#phone').val(data.ta.phone)
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
            populateTA()
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
var apiUrl = 'http://127.0.0.1:5000/api/';
var TA_APPLY_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/TAApplication.html"
var MY_APPS_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/TASplash.html"

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

function myAppsRedirect(){
  var url= window.location.href;
  var splitIndex = url.indexOf("?");
  var info = '';
  if(splitIndex !=-1){
    info = url.slice(splitIndex);
  }
  var newUrl = MY_APPS_REDIRECT_URL + info;
  window.location.href = newUrl;

}

function applyRedirect(){
  var url= window.location.href;
  var splitIndex = url.indexOf("?");
  var info = '';
  if(splitIndex !=-1){
    info = url.slice(splitIndex);
  }
  var newUrl = TA_APPLY_REDIRECT_URL + info;
  window.location.href = newUrl;
}

function editInfo(){
  var data = {}

  data.firstName = document.getElementById('first_name').value;
  data.lastName = document.getElementById('last_name').value;
  data.id= document.getElementById('ID').value;
	data.major = document.getElementById('major').value;
  data.cum_gpa = document.getElementById('cum_gpa').value;
  data.expected_grad= document.getElementById('expected_grad').value;
	data.prev_TA= document.getElementById('prev_Ta').value;
	data.phone= document.getElementById('phone').value;


  var onSuccess = function(e){
    alert('Yay')
  }

  var onError = function(e){
    alert('awww')
  }

  makePostRequest('editTA', data, onSuccess, onError)
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
