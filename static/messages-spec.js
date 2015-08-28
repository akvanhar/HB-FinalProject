
describe("delete message function", function () {
	beforeEach(function() {
		jasmine.Ajax.install();
		
	});
	
	afterEach(function() {
		jasmine.Ajax.uninstall();
	});

    it("should call the function when the button is clicked", function() {

		deleteMessage({currentTarget: $(".deleteButton")[0]}).toBeDefined()
    });

}); //close describe delete
