function deleteMessage() {
	alert("delete! Ha. Not. {{message.message_id}}");
	var message_id = {{ message.message_id }};
	$.post("/delete_message", message_id, function (result) {
		$("#message_sent").html('Your message has been deleted.')
		$("#message_sent").delay(3000).html('');
	})//end ajax post method
} //end deleteMessage function

$('#deletemessage{{ message.message_id }}').on('click', deleteMessage)