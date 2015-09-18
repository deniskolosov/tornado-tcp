$(document).ready(function() {
	if (!window.console) window.console = {};
	if (!window.console.log) window.console.log = function() {};

	$("#message").select();
	(function poll() {
		$.ajax({
			url: "/msg",
			type: "GET",
			success: function(data) {
				console.log(data);
				$('#msg').append('[' + data["lines"][0] + '] ');	
				for (var i = 0; i < data["lines"].length; i++) {
					$('#msg').append(data["lines"][i] + '|');	
				}

			},
			dataType: "text",
			complete: setTimeout(function() {poll()}, 3000),
			timeout: 3000

		})

	})();




});
