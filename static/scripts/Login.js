
var Tracker = (function() {

        // PRIVATE VARIABLES

        // The backend we'll use for Part 2. For Part 3, you'll replace this
        // with your backend.

        var apiUrl = 'http://127.0.0.1:5000/api/';

        // FINISH ME (Task 4): You can use the default smile space, but this means
        //            that your new smiles will be merged with everybody else's
        //            which can get confusing. Change this to a name that
        //            is unlikely to be used by others.
        var loginForm;
        var signUpForm;
        var buttons;
        var studentSignUp;
        var isProfessor;


         $(document).ready(function() {
    $('select').material_select();
  });
        // PRIVATE METHODS

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
                success: function(data, textStatus){
                  if(data.redirect){
                    window.location.href = data.redirect;
                  }
                },
                error: onFailure
            });
        };
/*
        var attachSignUpButtonHandler = function(e)
        {
            loginForm.on('click', '.signUpLink', function(e){
                loginForm.hide();
                signUpForm.show();
                if(isProfessor) studentSignUp.hide();
                else{
                    $('.login').css("transform","translate(-50%,-55%)")
                    $('.login').css("-webkit-transform","translate(-50%,-55%)")
                }
            });
            signUpForm.on('click', '.signUpSubmitButton', function(e){
                e.preventDefault();
                if(isProfessor){
                    var professor = {};
                    professor.id = signUpForm.find('.wsuIdInput').val();
                    professor.firstName = signUpForm.find('.firstNameInput').val();
                    professor.lastName = signUpForm.find('.lastNameInput').val();
                    professor.email = signUpForm.find('.emailInput').val();
                    professor.password = signUpForm.find('.passwordInput').val();
                    var onSuccess=function(data){
                        //redirect
                    }
                    var onFailure=function(){
                        //print failure
                    }
                    makePostRequest(apiUrl+'createProf',professor,onSuccess,onFailure);
                }
                else{//potentialTA
                    var TA = {};
                    TA.id = signUpForm.find('.wsuIdInput').val();
                    TA.firstName = signUpForm.find('.firstNameInput').val();
                    TA.lastName = signUpForm.find('.lastNameInput').val();
                    TA.email = signUpForm.find('.emailInput').val();
                    TA.password = signUpForm.find('.passwordInput').val();
                    TA.major = signUpForm.find('majorInput').val();
                    TA.gpa = signUpForm.find('gpaInput').val();
                    TA.gradDate = signUpForm.find('gradDateSelect').text();
                    var onSuccess=function(data){
                        //redirect
                    }
                    var onFailure=function(){
                        //print failure
                    }
                    makePostRequest(apiUrl+'createProf',professor,onSuccess,onFailure);
                }
            });
        }
*/



        /**
         * Start the app by displaying the most recent smiles and attaching event handlers.
         * @return {None}
         */
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
