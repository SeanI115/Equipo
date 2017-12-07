
var Tracker = (function() {
        $(document).ready(function() {
          $('select').material_select();
        });

        var id;
        var role;
        var classes;
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

                var insertApps = function(toInsert){
                  var header = '<a class="collection-item" id="'
                  header += toInsert.id+'">'
                  var classTitle = toInsert.prefix+toInsert.courseNumber;
                  var section = toInsert.labSection;
                  var semester = toInsert.semester;
                  var prof = toInsert.profLastName+', '+toInsert.profFirstName;
                  var statusBool = toInsert.accepted;
                  var statusStr = "";
                  if (statusBool == true){
                    statusStr = "Accepted";
                  }
                  else{
                    statusStr = "Pending";
                  }
                  classStr = header+classTitle+' '+semester+' '+section+' '+prof+' '+statusStr+'</a>'
                  classes.append(classStr)
                }

                var displayTAApps = function(){

                  var onSuccess=function(data)
                  {
                    for(var i = 0; i < data.apps.length;i++){
                      insertApps(data.apps[i])
                    }
                  }

                  var onError=function()
                  {

                  }

                  makeGetRequest('AppsByTAID/'+id, onSuccess, onError);

                };
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
            classes = $("#applications")
            displayTAApps()
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
var apiUrl = 'http://127.0.0.1:5000/api/';
var MY_INFO_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/TAInfo.html"
var APPLICATION_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/TAApplication.html"

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
var LOG_OUT_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/login.html"
function logoutRedirect(){
  window.location.href = LOG_OUT_REDIRECT_URL
}
function applicationRedirect(){
  var url= window.location.href;
  var splitIndex = url.indexOf("?");
  var info = '';
  if(splitIndex !=-1){
    info = url.slice(splitIndex);
  }
  var newUrl = APPLICATION_REDIRECT_URL + info;
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
