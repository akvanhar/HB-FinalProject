describe("delete message function", function () {

    it("should call the function when the button is clicked", function() {

    var fakeElement = $("<button class='deleteButton btn btn-xs' data-id='delete42'>Delete</button></");
    spyOn(fakeElement, 'deletemessage');
    expect(fakeElement.deleteMessage).toHaveBeenCalled()


    });
//     }//closes deleteMessageTest
});//close describe

