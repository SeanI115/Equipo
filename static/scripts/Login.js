
var Tracker = (function() {
    
        // PRIVATE VARIABLES
            
        // The backend we'll use for Part 2. For Part 3, you'll replace this 
        // with your backend.
    
        var apiUrl = 'https://mahan-warmup.herokuapp.com';
    
        // FINISH ME (Task 4): You can use the default smile space, but this means
        //            that your new smiles will be merged with everybody else's
        //            which can get confusing. Change this to a name that 
        //            is unlikely to be used by others. 
        var form;
        var buttons;
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
            form.hide();
            buttons.on('click', '.taButton', function(e){
                buttons.hide();
                form.show();
                isProfessor = false;
            });
            buttons.on('click', '.professorButton', function(e){
                buttons.hide();
                form.show();
                isProfessor = true;
            });
        }

        /**
         * Start the app by displaying the most recent smiles and attaching event handlers.
         * @return {None}
         */
        var start = function() {
            buttons = $(".loginButtons");
            form = $(".loginForm");
    
            attachStudentProfessorButtonHandler();
        };
        
    
        // PUBLIC METHODS
        // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
        return {
            start: start
        };
        
    })();
    