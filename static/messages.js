$(document).ready(function() {
	if (!window.console) window.console = {};
	if (!window.console.log) window.console.log = function() {};
    var entityMap = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': '&quot;',
        "'": '&#39;',
        "/": '&#x2F;'
    };
    function escapeHtml(string) {
        return String(string).replace(/[&<>"'\/]/g, function (s) {
            return entityMap[s];
        });
    }

	$("#message").select();
	(function poll() {
		$.ajax({
			url: "/msg",
			type: "GET",
			success: function(data) {
				console.log(data);
                $.each(data, function(k, v) {
                    if(k === 'Auth'){ return true; }
                    if(k === 'current_connections'){ return true; }
                    $('#msg')
                    .append('<h5>' + '[' + data['Auth'] + '] ' + escapeHtml(k) +
                            ' | ' + escapeHtml(v) + '<br>' + '<h5>');
                });
                $('#conns').empty();
                $.each(data['current_connections'], function(i, v) {
                    $('#conns').append('<div>' + v + '</div>');
                });
			},
			dataType: "json",
			complete: setTimeout(function() {poll()}, 3000),
			timeout: 3000

		})

	})();




});
