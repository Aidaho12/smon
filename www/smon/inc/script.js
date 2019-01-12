$( function() {
	$('#sort_by_status').click(function() {
		sort_by_status();
	});	
});

function sort_by_status() {
	$('<div id="good_services"></div>').appendTo('.main');
	$(".good").prependTo("#good_services");	
}