
  var Tracker = (function() {


    var apiUrl = 'http://127.0.0.1:5000';

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

    var data = {
    'foo': 'bar',
    'foo2': 'baz'
    }

    var displayApps = function() {

      var onSuccess = function(data) {

          var appDrop = $(".appDrop");

          var app = $('<select />');
          for(var val in data) {

              $('<option />', {value: val, text: data[val]}).appendTo(app);

            }

          app.appendTo(appDrop); // or wherever it should be

        };
      var onFailure = function() {


        };

      makeGetRequest('AppsForClass',onSuccess,onFailure);

    };

    var displayClass = function() {

      var onSuccess = function(data) {

          var appDrop = $(".appDrop");

          var app = $('<select />');
          for(var val in data) {

              $('<option />', {value: val, text: data[val]}).appendTo(app);

            }

          app.appendTo(appDrop); // or wherever it should be

        };
      var onFailure = function() {


        };

      makeGetRequest('AppsForClass',onSuccess,onFailure);

    };



    /**
     * Start the app by attaching event handlers.
     * @return {None}
     */
    var start = function() {

        //attachLoginButtonHandler();
    };


    // PUBLIC METHODS
    // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
    return {
        start: start
    };


  })();
