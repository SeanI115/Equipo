
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
                success: onSuccess,
                error: onFailure
            });
        };

        var attachStudentProfessorButtonHandler = function(e)
        {
            loginForm.hide();
            signUpForm.hide();
            buttons.on('click', '.taButton', function(e){
                buttons.hide();
                loginForm.show();
                $('.errorMessage').hide();
                isProfessor = false;
            });
            buttons.on('click', '.professorButton', function(e){
                buttons.hide();
                loginForm.show();
                $('.errorMessage').hide();
                isProfessor = true;
            });
        }

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

                    }
                    var onFailure=function(){
                        //print failure
                    }
                    makePostRequest(apiUrl+'createProf',professor,onSuccess,onFailure);
                }
                else{//potentialTA
                    var ta = {};
                    ta.id = signUpForm.find('.wsuIdInput').val();
                    ta.firstName = signUpForm.find('.firstNameInput').val();
                    ta.lastName = signUpForm.find('.lastNameInput').val();
                    ta.email = signUpForm.find('.emailInput').val();
                    ta.password = signUpForm.find('.passwordInput').val();
                    ta.major = signUpForm.find('.majorInput').val();
                    ta.gpa = signUpForm.find('.gpaInput').val();
                    ta.gradDate = signUpForm.find('.gradDateSelect').val();
                    var onSuccess=function(data){



                    }
                    var onFailure=function(){

                        console.error('create smile failed');

                    }
                    makePostRequest(apiUrl+'createTA',ta,onSuccess,onFailure);
                }
            });
        }

        /**
         * Start the app by displaying the most recent smiles and attaching event handlers.
         * @return {None}
         */
        var start = function() {
            buttons = $(".loginButtons");
            loginForm = $(".loginForm");
            signUpForm = $(".signUpForm");
            studentSignUp = $(".student");

            attachStudentProfessorButtonHandler();
            attachSignUpButtonHandler();
            //attachLoginButtonHandler();
        };


        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };

    })();
