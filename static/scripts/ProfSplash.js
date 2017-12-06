
var Tracker = (function() {
        $(document).ready(function() {
          $('select').material_select();
        });

        var id;
        var role;

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

        var insertClass = function(toInsert){}

        var displayProfClasses = function(){
          var classes= getClassesForProf();
          for(var i = 0; i <classes.length; i++){
            insertClass(classes[i]);
          }
        }

        var getClassesForProf = function(){
          apiFunction='ClassesByProfID'
          var onSuccess=function(data)
          {
            return data.classes;
          }

          var onError=function()
          {
            return []
          }

          makeGetRequest('ClassesByProfID/'+id+'/'+role+'/', onSuccess, onError);
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
            //displayProfClasses();
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();

var MY_INFO_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfInfo.html"
var CREATE_COURSE_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfCourseCreate.html"
var MANAGE_TAS_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/ProfTAPicker.html"

function courseCreateRedirect(){
  var url= window.location.href;
  var splitIndex = url.indexOf("?");
  var info = '';
  if(splitIndex !=-1){
    info = url.slice(splitIndex);
  }
  var newUrl = CREATE_COURSE_REDIRECT_URL + info;
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




var apiUrl = 'http://127.0.0.1:5000/api/';
