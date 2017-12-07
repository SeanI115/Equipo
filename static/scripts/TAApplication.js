
var Tracker = (function() {
        $(document).ready(function() {
          $('select').material_select();
        });

        var id;
        var role;
        var prefixSelector;

        var getParameterByName = function(name, url) {
            if (!url) url = window.location.href;
            name = name.replace(/[\[\]]/g, "\\$&");
            var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, " "));
        }

        var makeGetRequest = function(url, onSuccess, onFailure) {
            $.ajax({
                type: 'GET',
                url: apiUrl + url,
                dataType: "json",
                success: onSuccess,
                error: onFailure
            });
        };

        var populatePrefixSelector = function() {
          var onSuccess = function(data){
            prefixes = data.prefixes
            for(var i = 0; i < prefixes.length; i++)
            {
              newOption = "<a class='collection-item' onClick=findClassesForPrefix(this) id='"+prefixes[i]+"'>"+prefixes[i]+"</a>"
              prefixSelector.append(newOption);
            }
          }

          var onError = function(){
            alert('boo')
          }

          makeGetRequest('ClassPrefixes', onSuccess, onError)
        }

        var start = function() {
            id = getParameterByName('id')
            role = getParameterByName('role')
            prefixSelector = $('#prefixSelector')
            $('#courseSelectorDiv').hide()
            $("#applicationDiv").hide()
            populatePrefixSelector()
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
var classID;

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

function findClassesForPrefix(item){
  $('#courseSelectorDiv').show()
  $('#prefixDiv').hide()
  prefix = item.id
  id = getParameterByNamePub('id')
  role = getParameterByNamePub('role')
  callURL = 'ClassesByPrefix/'+prefix+'/'+id+'/'+role
  var onSuccess = function(data){
    classes = data.classes
    for(var i = 0; i < classes.length; i++)
    {
      insertClass(classes[i])
    }
  }

  var onFailure = function(){

  }

  makeGetRequest(callURL, onSuccess, onFailure)

}

function insertClass(toInsert){
    var header = '<a class="collection-item" onClick=apply(this) id="'
    header += toInsert.id+'">'
    var classTitle = toInsert.prefix+toInsert.courseNumber;
    var section = toInsert.labSection;
    var semester = toInsert.semester;
    var tas = toInsert.numTAsAdded+'/'+toInsert.numTAsNeeded+"TAs";
    var prof = toInsert.lastName+', '+toInsert.firstName;
    classStr = header+classTitle+' '+semester+' '+section+' '+tas+' '+prof+'</a>'
    $('#courseSelector').append(classStr)
}

function apply(toApply){
  classID = toApply.id
  $("#courseSelectorDiv").hide()
  $("#applicationDiv").show()

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

var LOG_OUT_REDIRECT_URL = "file:///Users/samuelmahan/Desktop/Fall17/CS322/TATracker/static/login.html"
function logoutRedirect(){
  window.location.href = LOG_OUT_REDIRECT_URL
}

function submitApp(item){
  var data = {}
  data.studentID = getParameterByNamePub('id')
  data.classID = classID
  data.gradeInClass = document.getElementById('gradeInClass').value
  data.story = document.getElementById('story').value

  var onSuccess = function(){
    applicationRedirect()
  }

  var onFailure = function(){

  }

  makePostRequest('createApplication', data, onSuccess, onFailure);
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




var apiUrl = 'http://127.0.0.1:5000/api/';
