var Smile = (function() {

    // PRIVATE VARIABLES

    // The backend we'll use for Part 2. For Part 3, you'll replace this
    // with your backend.
    var apiUrl = 'http://127.0.0.1:5000';
    // FINISH ME (Task 4): You can use the default smile space, but this means
    //            that your new smiles will be merged with everybody else's
    //            which can get confusing. Change this to a name that
    //            is unlikely to be used by others.
    var smileSpace = 'initial'; // The smile space to use.
    var smiles; // smiles container, value set in the "start" method below
    var smileTemplateHtml; // a template for creating smiles. Read from index.html
                           // in the "start" method
    var create; // create form, value set in the "start" method below


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
     * @param  {string}   url       URL path
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


     // Handler for Updating TA Information
      @return {None}

    var attachLikeHandler = function(e) {
        // Attach this handler to the 'click' action for elements with class 'inputSubmit'
        smiles.on('click', '.inputSubmit', function(e) {
            // FINISH ME (Task 3): get the id of the smile clicked on to use in the POST request
            var smileId = $(this).parents('article').attr('id');
            // Prepare the AJAX handlers for success and failure
            var onSuccess = function(data) {
                /* FINISH ME (Task 3): update the like count in the UI */
                $('#'+smileId).find('.count').text(data.smile.like_count);
            };
            var onFailure = function() {
                console.error('like smile error');
            };
            /* FINISH ME (Task 3): make a POST request to like this smile */
            makePostRequest('/api/smiles/'+smileId+'/like', {}, onSuccess, onFailure);
        });
    };

    /**
     * Insert smile into smiles container in UI
     * @param  {Object}  smile       smile JSON
     * @param  {boolean} beginning   if true, insert smile at the beginning of the list of smiles
     * @return {None}
     */
    var insertSmile = function(smile, beginning) {
        // Start with the template, make a new DOM element using jQuery
        var newElem = $(smileTemplateHtml);
        // Populate the data in the new element
        // Set the "id" attribute
        newElem.attr('id', smile.id);
        // Now fill in the data that we retrieved from the server
        newElem.find('.title').text(smile.title);
        newElem.find('.story').text(smile.story);
        newElem.find('.count').text(smile.like_count);


        var post_date = new Date(smile.created_at);
        var month = post_date.getMonth() + 1;
        var date = 'Posted at: ' + post_date.getHours() + ':' + post_date.getMinutes()
                + ' on ' + month + '/' + post_date.getDate() + '/' + post_date.getFullYear();

        newElem.find('.timestamp').text(date);


        if(smile.happiness_level==1)
        {
            newElem.find('.happiness-level').removeClass('.happiness-level-1').addClass('.happiness-level-1');
        }
        else if(smile.happiness_level==2)
        {
            newElem.find('.happiness-level').removeClass('.happiness-level-1').addClass('.happiness-level-2');
        }
        else if(smile.happiness_level==3)
        {
            newElem.find('.happiness-level').removeClass('.happiness-level-1').addClass('.happiness-level-3');
        }
        // FINISH ME (Task 2): fill-in the rest of the data
        if (beginning) {
            smiles.prepend(newElem);
        } else {
            smiles.append(newElem);
        }
    };


     /**
     * Get recent smiles from API and display 10 most recent smiles
     * @return {None}
     */
    var displaySmiles = function() {
        // Prepare the AJAX handlers for success and failure
        var onSuccess = function(data) {
            /* FINISH ME (Task 2): display smiles with most recent smiles at the beginning */
            for(var i = 0; i < data.smiles.length; i++){

                insertSmile(data.smiles[i], false);
            }

        };
        var onFailure = function() {
            console.error('display smiles failed');
        };
        /* FINISH ME (Task 2): make a GET request to get recent smiles */

        makeGetRequest('/api/smiles?space=initial&count=5&order_by=created_at', onSuccess, onFailure);
    };


    /**
     * Add event handlers for submitting the create form.
     * @return {None}
     */
    var attachCreateHandler = function(e) {
        // First, hide the form, initially
        create.find('.smile-form').hide();

        // FINISH ME (Task 4): add a handler to the 'Share a smile...' button to
        //                     show the 'form' and hide to button
        create.on('click', '.link', function (e) {
           create.find('.smile-form').show();
           smiles.hide();
        });


        // FINISH ME (Task 4): add a handler for the 'Cancel' button to hide the form
        // and show the 'Shared a smile...' button
        //create.on('click', '.')

        // The handler for the Post button in the form
        create.on('click', '.submit-input', function (e) {
            e.preventDefault (); // Tell the browser to skip its default click action

            var error_title = false, error_story = false, error_lvl = false;

            var smile = {}; // Prepare the smile object to send to the server
            smile.title = create.find('.title-input').val();
            if(smile.title.length > 64 || smile.title == 0) error_title = true;
            smile.story = create.find('.story-input').val();
            if(smile.story.length > 2048 || smile.title == 0) error_story = true;
            smile.like_count = 0;
            smile.space = 'initial';
            var item = $('.drop-input').find('option:selected').text();
            if(item == 'Happy') smile.happiness_level = 1;
            else if (item == "Really happy") smile.happiness_level = 2;
            else smile.happiness_level = 3;
            if(smile.happiness_level > 3 || smile.happiness_level < 1) error_lvl = true;

            // FINISH ME (Task 4): collect the rest of the data for the smile
            var onSuccess = function(data) {
                // FINISH ME (Task 4): insert smile at the beginning of the smiles container
                insertSmile(smile, true);
            };
            var onFailure = function() {
                console.error('create smile failed');
            };

            // FINISH ME (Task 4): make a POST request to create the smile, then
            //            hide the form and show the 'Shared a smile...' button

            if(error_title)
             {
                if(smile.title.length==0) alert("You need a title!");
                else if(smile.title.length > 64) alert("Your title is too long!");
             }
            else if(error_story)
             {
                if(smile.story.length==0) alert("You need a story!");
                else if(smile.story.length > 2048) alert("Your story is too long!");
             }
            else if(error_lvl) alert("You need a happiness level of 1, 2, or 3");

            else makePostRequest('/api/smiles/', smile, onSuccess, onFailure);
        });

    };


    /**
     * Start the app by displaying the most recent smiles and attaching event handlers.
     * @return {None}
     */
    var start = function() {
        smiles = $(".smiles");
        create = $(".create");

        // Grab the first smile, to use as a template
        smileTemplateHtml = $(".smiles .smile")[0].outerHTML;
        // Delete everything from .smiles
        smiles.html('');

        displaySmiles();
        attachLikeHandler();
        attachCreateHandler();
    };


    // PUBLIC METHODS
    // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
    return {
        start: start
    };

})();
