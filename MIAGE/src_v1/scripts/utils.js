/// Useful functions
(function(Utils){  

    function intToSizedStr(n, len) {
		var s = ""+n;
		while(s.length < len) {
			s = "0" + s;
		}
		return s;
    }

    Utils.secondsToHourMinute = function(seconds) {
		var hours = 0|(seconds / 3600);
		var minutes = (0|(seconds / 60)) % 60;
		return intToSizedStr(hours, 2) + "h" + intToSizedStr(minutes, 2);
	}
	Utils.secondsToHourMinuteSecond = function(seconds) {
		var hours = 0|(seconds / 3600);
		var minutes = (0|(seconds / 60)) % 60;
		var remainingSeconds = seconds-(hours * 3600 + minutes * 60);
		var result = "";
		if (hours > 0){
			result = intToSizedStr(hours, 2) + "h"
		}
		result +=  intToSizedStr(minutes, 2) + "m" + intToSizedStr(remainingSeconds, 2) + "s";

		return result; 
	}


}(window.Utils = window.Utils || {}));