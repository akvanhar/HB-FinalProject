function loadMap(evt){
	$("#tableButton").removeClass('active');
	$("#tableButton").removeAttr('autofocus');
	$("#mapButton").attr('autofocus');
	$("#mapButton").addClass('active');
	$("#listingsTable").css("display", "none");
	$("#listingsMap").css("display", "block");
}
$("#mapButton").on('click', loadMap);

function loadTable(evt){
	$("#mapButton").removeClass('active');
	$("#mapButton").removeAttr('autofocus');
	$("#tableButton").attr('autofocus');
	$("#tableButton").addClass('active');
	$("#listingsTable").css("display", "block");
	$("#listingsMap").css("display", "none");
}
$("#tableButton").on('click', loadTable);