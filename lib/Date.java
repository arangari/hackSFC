public class Date {

	public static Date newInstance(Integer year, Integer month, Integer day){
		return new Date();
	}

	public static Integer daysInMonth(Integer year, Integer month){
		return 1;
	}


	public static Boolean isLeapYear(Integer year){
		return true;
	}

	public Date addDays(Integer additionalDays){
		return new Date();
	}

	public Date addMonths(Integer additionalMonths){
		return new Date();
	}

	public Date addYears(Integer additionalYears){
		return new Date();
	}

	public Integer dayOfYear(){
		return 1;
	}

	public Integer daysBetween( Date secondDate){
		return 1;
	}

	public String format(){
		return null;
	}

	public Boolean isSameDay(Date dateToCompare){
		return true;
	}

	public Integer monthsBetween(Date secondDate){
		return 1;
	}

	/*newInstance(year, month, date)
Constructs a Date from Integer representations of the year, month (1=Jan), and day.
parse(stringDate)
Constructs a Date from a String. The format of the String depends on the local date format.
today()
Returns the current date in the current user's time zone.
toStartOfMonth()
Returns the first of the month for the Date that called the method.
toStartOfWeek()
Returns the start of the week for the Date that called the method, depending on the context user's locale.
valueOf(stringDate)
Returns a Date that contains the value of the specified String.
valueOf(fieldValue)
Converts the specified object to a Date. Use this method to convert a history tracking field value or an object that represents a Date value.
year()
Returns the year component of a Date
	 */

}
