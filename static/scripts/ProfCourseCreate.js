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


        var buttons;
        var courseForm;

        attachCreateHandler = function(e) {


          $('.messages').hide();


          signUpForm.on('click', '.courseCreateSubmitButton', function(e){

              e.preventDefault();

              var classOb = {};

              classOb.prefix = courseForm.find('.subjectInput').val();
              classOb.courseNumber = courseForm.find('.numberInput').val();
              classOb.description = courseForm.find('.descriptionInput').val();
              classOb.year = courseForm.find('.yearInput').val();
              classOb.semester = courseForm.find('.semesterInput').val();
              classOb.sections = courseForm.find('.sectionInput').val();
              classOb.day = courseForm.find('.dayInput').val();
              classOb.time = courseForm.find('.timeInput').val();


              var onSuccess=function(data){
                $('.messages').show();
                $('.errorMessage').hide();
              }
              var onFailure=function(){

                $('.messages').show();
                $('.successMessage').hide();
              }

              makePostRequest('createClass',class,onSuccess,onFailure);
          });


          signUpForm.on('click', '.messageOKButton', function(e){

              $('.messages').hide();

          });



        }

        /**
         * Start the app by displaying the most recent smiles and attaching event handlers.
         * @return {None}
         */
        var start = function() {
            buttons = $(".button");
            courseForm = $(".CourseCreateForm");

            attachCreateHandler();
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
