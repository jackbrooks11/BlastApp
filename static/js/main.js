$(function() {
    $('#submitForm').on('submit', function(e) {
        $('#loading').show();
        $('#errors').hide();
        $('#noResults').hide();
    });
});