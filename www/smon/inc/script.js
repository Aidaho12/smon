$( function() {
	$('#sort_by_status').click(function() {
		sort_by_status();
	});	
});

function sort_by_status() {
	$('<div id="good_services"></div>').appendTo('.main');
	$(".good").prependTo("#good_services");	
}
function secToTime(sec){
    dt = new Date();
    dt.setTime(sec*1000);
    return dt.getUTCHours()+"h "+dt.getUTCMinutes()+"m "+dt.getUTCSeconds()+"s";
} 