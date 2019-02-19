$( function() {
	$('#sort_by_status').click(function() {
		sort_by_status();
	});	
});

function sort_by_status() {
	$('<div id="err_services"></div>').appendTo('.main');
	$('<div id="good_services"></div>').appendTo('.main');
	$(".good").prependTo("#good_services");	
	$(".err").prependTo("#err_services");	
	$('.group').remove();
	$('.group_name').detach();
	
	
}
function secToTime(sec){
    dt = new Date();
    dt.setTime(sec*1000);
    return Math.floor(sec/60/60/24)+"d "+ dt.getUTCHours()+"h "+dt.getUTCMinutes()+"m "+dt.getUTCSeconds()+"s";
} 