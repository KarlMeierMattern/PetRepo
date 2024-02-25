$(document).ready(function() {
    // AJAX request for health
    $('button.user_info.health').click(function() {
        var textBoxContainerId = 'healthTextBoxContainer';
        var $textBoxContainer = $('#' + textBoxContainerId);
        
        // Toggle visibility of the textbox container
        $textBoxContainer.toggle();

        // Check if the textbox container is visible after toggling
        if ($textBoxContainer.is(':visible')) {
            // Make an AJAX request to get the textbox content
            $.ajax({
                url: '/get_health_textbox',
                method: 'GET',
                success: function(response) {
                    var htmlContent = response.html_content;
                    $textBoxContainer.html(htmlContent);
                },
                error: function(xhr, status, error) {
                    console.error("AJAX request failed:", error);
                }
            });
        }
    });

    // AJAX request for behaviour
    $('button.user_info.behaviour').click(function() {
        var textBoxContainerId = 'behaviourTextBoxContainer';
        var $textBoxContainer = $('#' + textBoxContainerId);
        
        // Toggle visibility of the textbox container
        $textBoxContainer.toggle();

        // Check if the textbox container is visible after toggling
        if ($textBoxContainer.is(':visible')) {
            // Make an AJAX request to get the textbox content
            $.ajax({
                url: '/get_behaviour_textbox',
                method: 'GET',
                success: function(response) {
                    var htmlContent = response.html_content;
                    $textBoxContainer.html(htmlContent);
                },
                error: function(xhr, status, error) {
                    console.error("AJAX request failed:", error);
                }
            });
        }
    });

    // AJAX request for vet
    $('button.user_info.vet').click(function() {
        var textBoxContainerId = 'vetTextBoxContainer';
        var $textBoxContainer = $('#' + textBoxContainerId);
        
        // Toggle visibility of the textbox container
        $textBoxContainer.toggle();

        // Check if the textbox container is visible after toggling
        if ($textBoxContainer.is(':visible')) {
            // Make an AJAX request to get the textbox content
            $.ajax({
                url: '/get_vet_textbox',
                method: 'GET',
                success: function(response) {
                    var htmlContent = response.html_content;
                    $textBoxContainer.html(htmlContent);
                },
                error: function(xhr, status, error) {
                    console.error("AJAX request failed:", error);
                }
            });
        }
    });
    // AJAX request for contact
    $('button.user_info.contact').click(function() {
        var textBoxContainerId = 'contactTextBoxContainer';
        var $textBoxContainer = $('#' + textBoxContainerId);
        
        // Toggle visibility of the textbox container
        $textBoxContainer.toggle();

        // Check if the textbox container is visible after toggling
        if ($textBoxContainer.is(':visible')) {
            // Make an AJAX request to get the textbox content
            $.ajax({
                url: '/get_contact_textbox',
                method: 'GET',
                success: function(response) {
                    var htmlContent = response.html_content;
                    $textBoxContainer.html(htmlContent);
                },
                error: function(xhr, status, error) {
                    console.error("AJAX request failed:", error);
                }
            });
        }
    });
    $('button.user_info.address').click(function() {
        var textBoxContainerId = 'addressTextBoxContainer';
        var $textBoxContainer = $('#' + textBoxContainerId);
        
        // Toggle visibility of the textbox container
        $textBoxContainer.toggle();

        // Check if the textbox container is visible after toggling
        if ($textBoxContainer.is(':visible')) {
            // Make an AJAX request to get the textbox content
            $.ajax({
                url: '/get_address_textbox',
                method: 'GET',
                success: function(response) {
                    var htmlContent = response.html_content;
                    $textBoxContainer.html(htmlContent);
                },
                error: function(xhr, status, error) {
                    console.error("AJAX request failed:", error);
                }
            });
        }
    });
});



// When the button with the class user_info is clicked, jQuery's event handling mechanism listens 
// for the click event. Upon the click event, the jQuery code executes an AJAX request using $.ajax() 
// function. This function sends a request to the server endpoint /get_health_textbox.
// The server responds to the AJAX request by sending back JSON data containing the HTML content for 
// the text box. This JSON response is received by the client-side JavaScript code.
// The success callback function specified in the AJAX request (success: function(response) { ... }) 
// extracts the HTML content from the JSON response and inserts it into the 
// <div id="healthTextBoxContainer"></div> element on the page. This effectively renders the text box 
// below the button.

