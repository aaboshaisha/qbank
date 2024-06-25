document.addEventListener('DOMContentLoaded', (event) => {
    // Disable right-click context menu
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });

    // Disable copying
    document.addEventListener('copy', function(e) {
        e.preventDefault();
    });

    // Disable cutting
    document.addEventListener('cut', function(e) {
        e.preventDefault();
    });

    // Disable pasting
    document.addEventListener('paste', function(e) {
        e.preventDefault();
    });
});
