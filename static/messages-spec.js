describe("delete message function", function () {
	// beforeEach(function() {
 //      jasmine.Ajax.install();
 //    });
 //    afterEach(function() {
 //    	jasmine.Ajax.uninstall();
 //    });

    it("should make an AJAX request to the correct URL", function() {
    spyOn($, "post");

    expect($.post).toHaveBeenCalled()

    });
    
    // deleteMessageTest();
//     expect($.ajax.mostRecentCall.args[0]["url"]).toEqual("/delete_message");
// 	});

// function deleteMessageTest() {
//     $.post("/delete_message", messageId, function (result) {
// 		$("#messageSent").html('');
// 		$("#messageSent").css("display", "block");
// 		$("#messageSent").html('Your message has been deleted.');
// 		$("#messageSent").delay(3000).fadeOut();
// 		$("#message"+thisMessage).remove();
// 		$("#messageCount").html(result['new_messages']);
// 		});
//     }//closes deleteMessageTest
});//close describe
