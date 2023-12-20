function testEvent(e) {
	var test = e.currentTarget.id;
	return test;
}

function testDom() {
	var test = document.querySelector('#Test-2');
	var test = document.querySelector('#Asap-twenty-one');
	return test.value;
}

module.exports = {
	testEvent,
	testDom
};