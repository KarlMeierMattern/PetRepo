$(document).ready(function() {
    console.log("Document is ready."); // Log when the document is ready

    $('button.user_info').click(function() {
        console.log("Button clicked."); // Log when the button is clicked
        
        $.ajax({
            url: '/get_health_textbox',
            success: function(response) {
                console.log("AJAX request succeeded."); // Log when the AJAX request succeeds
                console.log("Response:", response); // Log the response data
                
                var htmlContent = response.html_content; // Access the 'html_content' key
                $('#healthTextBoxContainer').html(htmlContent);
            },
            error: function(xhr, status, error) {
                console.error("AJAX request failed:", error); // Log if the AJAX request fails
            }
        });
    });
});

// When the button with the ID healthButton is clicked, jQuery's event handling mechanism listens 
// for the click event. Upon the click event, the jQuery code executes an AJAX request using $.ajax() 
// function. This function sends a request to the server endpoint /get_health_textbox.
// The server responds to the AJAX request by sending back JSON data containing the HTML content for 
// the text box. This JSON response is received by the client-side JavaScript code.
// The success callback function specified in the AJAX request (success: function(response) { ... }) 
// extracts the HTML content from the JSON response and inserts it into the 
// <div id="healthTextBoxContainer"></div> element on the page. This effectively renders the text box 
// below the button.

