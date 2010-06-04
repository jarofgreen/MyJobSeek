
function showNextElement(element) {
	element.next().show();
}

function hideNextElement(element) {
	element.next().hide();
}

//############  calendar
MONTH_NAMES = new Array(
  'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
  'September', 'October', 'November', 'December'
)

// ########################

function updateCalendar(element) {
	fieldName = element.name.substr(0,  element.name.length-5);
	bits = element.value.split("-");
	if (bits[1].substr(0,1) == "0") bits[1] = bits[1].substr(1);
	if (bits[2].substr(0,1) == "0") bits[2] = bits[2].substr(1);
	year = parseInt(bits[0]);
	//if (isNaN(year)) alert("NO YEAR!");
	monthval = (parseInt(bits[1])- 1);
	//if (isNaN(monthval)) alert("NO MONTH!");
	date = parseInt(bits[2]);
	//if (isNaN(date)) alert("NO DATE!");
	$(fieldName+'_humanreadable').update(date + " " + MONTH_NAMES[monthval] + " "+year);
}


function SelectNewOrExistingWidgetChange(element) {
	if (element.selectedIndex == 0) {
		$('id_'+element.name+'_new').show();
	} else {
		$('id_'+element.name+'_new').hide();
	}
}

