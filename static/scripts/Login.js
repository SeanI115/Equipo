
var Tracker = (function() {

  $(document).ready(function() {
    $('select').material_select();
  });

        var start = function() {
            errorMessage = $("#errorMessage")
            errorMessage.hide();

        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();

var PROF_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfSplash.html"
var TA_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/TASplash.html"
var apiUrl = 'http://127.0.0.1:5000/api/';

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

function makeSignUpRequest()
{
  var isTA = document.getElementById("ta").checked;
  var data = {};
  data.firstName=document.getElementById("firstname").value;
  data.lastName=document.getElementById('lastname').value;
  data.id=document.getElementById('wsuID').value;
  data.email=document.getElementById('emailField').value;
  data.password=document.getElementById('passwordField').value;
  if(isTA){
    data.phone=document.getElementById('phone').value;
    data.major=document.getElementById('major').value;
    data.cum_gpa=document.getElementById('gpa').value;
    data.expected_grad=document.getElementById('gradDate').value;
    data.prev_TA=document.getElementById('prevTa').checked;
  }

  postURL = isTA ? 'createTA' : 'createProf';

  var onSuccess = function(data){
    redirectUrl = '';
    if(isTA)redirectUrl = TA_REDIRECT_URL;
    else redirectUrl = PROF_REDIRECT_URL;
    id=data.created.id;
    role = isTA ? 'ta' : 'prof';
    redirectUrl += '?id=' + id +'&role=' + role;
    window.location.replace(redirectUrl);
  }

  var onError = function(){

  }

  makePostRequest(postURL, data, onSuccess, onError);
}

function attemptLogin(buttonID)
{
  isProf = (buttonID=='loginProfButton')
  postURL = 'login'
  if(isProf) postURL += 'Prof'
  else postURL += 'TA'
  var data = {}
  data.email = $('#email').val();
  data.password = $('#password').val();

  var onSuccess = function(data){
  //redirect
  redirectUrl = '';
  if(isProf)redirectUrl = PROF_REDIRECT_URL;
  else redirectUrl = TA_REDIRECT_URL;
  id=data.loggedIn.id;
  role = isProf ? 'prof' : 'ta';
  redirectUrl += '?id=' + id +'&role=' + role;
  window.location.replace(redirectUrl);
  }

  var onError = function(){
    errorMessage.show();
    errorMessage.css({'color':'red'});
  }
  makePostRequest(postURL, data, onSuccess, onError);
};

function showThis(ta)
         {
            var gpashow= document.getElementById("taform");
            var gpashow2= document.getElementById("taform2");
            var gpashow3= document.getElementById("taform3");
            gpashow.style.display = ta.checked ? "block" : "none";
            gpashow2.style.display = ta.checked ? "block" : "none";
            gpashow3.style.display = ta.checked ? "block" : "none";
         };
