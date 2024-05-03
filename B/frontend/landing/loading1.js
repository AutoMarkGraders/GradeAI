// After the page is fully loaded
$(window).on('load', function() {
    // Play the animation for 5 seconds
    setTimeout(function() {
        // Hide the loading screen after animation completion
        $('#loading-screen').fadeOut('slow', function() {
            // Show the main content
            $('.cont').fadeIn('slow');
        });
    }, 5500); // Adjust the duration (in milliseconds) as needed
});