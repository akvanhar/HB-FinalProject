function deleteMessage(evt) {
	//delete the user message and display success message
	targetMessage = $(evt.currentTarget).data().id;
	var thisMessage = targetMessage.slice(6);
	var messageId = { message_id: thisMessage };
	$.post("/delete_message", messageId, function (result) {
		$("#messageSent").html('');
		$("#messageSent").css("display", "block");
		$("#messageSent").html('Your message has been deleted.');
		$("#messageSent").delay(3000).fadeOut();
		$("#message"+thisMessage).remove();
		});
}
$('.deleteButton').click(deleteMessage);

function reply(evt) {
	//submit the form to the server and close the modal window
	evt.preventDefault();
	targetModal = $(evt.currentTarget).data().id;
	var thisModal = targetModal.slice(6);
	messageInfo = $("#replyTo"+thisModal).serialize();

	$.post("/reply_to_message", messageInfo, function (result) {
		// Display a success message
		$("#textArea"+thisModal).val("");
		$("#myModal"+thisModal).modal('hide');
		$("#messageSent").html('');
		$("#messageSent").css("display", "block");
		$("#messageSent").html(result);
		$("#messageSent").delay(3000).fadeOut();
		});
}
$('.modalSubmit').click(reply);

function toggleRead(evt) {
	targetMessage = $(evt.currentTarget).data().id;
	var thisMessageId = targetMessage.slice(4);
	var messageId = { message_id: thisMessageId };
	$.post("/toggle_read", messageId, function (result) {
		if (result['read_status'] === true) {
			// display a success message
			$("#messageSent").html('');
			$("#messageSent").css("display", "block");
			$("#messageSent").html('Your message has been marked as read.');
			$("#messageSent").delay(3000).fadeOut();
			// change the class and change the button
			$(evt.currentTarget).html("Mark as unread");
			$("#message"+thisMessageId).removeClass('unreadMessage');
			$("#message"+thisMessageId).addClass('readMessage');
		} else {
			// display a success message
			$("#messageSent").html('');
			$("#messageSent").css("display", "block");
			$("#messageSent").html('Your message has been marked as unread.');
			$("#messageSent").delay(3000).fadeOut();
			// chage the class and change the button
			$(evt.currentTarget).html("Mark as read");
			$("#message"+thisMessageId).removeClass('readMessage');
			$("#message"+thisMessageId).addClass('unReadMessage');
		}
		$("#messageCount").html(result['new_messages']);
	});
}

$('.readStatusButton').click(toggleRead);

function sendText(evt) {
	targetMessage = $(evt.currentTarget).data().id;
	var thisMessageId = targetMessage.slice(4);
	var messageId = { message_id: thisMessageId };

}

$('.textButton').click(sendText);