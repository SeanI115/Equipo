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


          $('.errorMessage').hide();


          signUpForm.on('click', '.courseCreateSubmitButton', function(e){

              e.preventDefault();

              var class = {};

              class.prefix = courseForm.find('.subjectInput').val();
              class.courseNumber = courseForm.find('.numberInput').val();
              class.description = courseForm.find('.descriptionInput').val();
              class.year = courseForm.find('.yearInput').val();
              class.semester = courseForm.find('.semesterInput').val();
              class.sections = courseForm.find('.sectionInput').val();
              class.day = courseForm.find('.dayInput').val();
              class.time = courseForm.find('.timeInput').val();


              var onSuccess=function(data){

              }
              var onFailure=function(){

                    
              }

              makePostRequest('createClass',class,onSuccess,onFailure);

              window.location.href = "ProfSplash.html"

          });



        };

        /**
         * Start the app by displaying the most recent smiles and attaching event handlers.
         * @return {None}
         */
        var start = function() {
            buttons = $(".button");
            courseForm = $(".CourseCreateForm");

            attachStudentProfessorButtonHandler();
            //attachLoginButtonHandler();
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
