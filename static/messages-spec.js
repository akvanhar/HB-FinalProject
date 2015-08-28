var response;
describe("test ajax calls", function() {
describe("delete message function", function () {
	beforeEach(function() {
		jasmine.Ajax.install();
		
	});
	
	afterEach(function() {
		jasmine.Ajax.uninstall();
	});

    it("should call the function when the button is clicked", function() {
    	var doneFn = jasmine.createSpy("success");


		function deleteMessage() {
			var messageId = { message_id: 262 };
			$.post("/delete_message", messageId, function (result) {
				response = result;
				});
		}

		deleteMessage();

    	// var xhr = new XMLHttpRequest();
     //  	xhr.onreadystatechange = function(args) {
     //    	if (this.readyState == this.DONE) {
     //      		doneFn(this.responseText);
     //    	}
     //  	};

     //  	xhr.open("POST", "/delete_message?message_id=262");
     //  	xhr.send();
     //  	var data = xhr.data();
     //  	console.log(data);


      	var testcall = jasmine.Ajax.requests.mostRecent();
      	expect(testcall.url).toBe('/delete_message');
      	console.log(testcall.data());
      	console.log(response);
      	expect(doneFn).not.toHaveBeenCalled();

      	// jasmine.Ajax.requests.mostRecent().response({
      	// 	"status": 200
      	// });
    	console.log(jasmine.Ajax.requests.mostRecent().response);

    });

}); //close describe delete
}); //close describe Ajax