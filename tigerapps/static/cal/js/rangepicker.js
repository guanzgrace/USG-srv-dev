/* Enables range selection on the standard jQueryUI datepicker
 * Source (modified): http://www.tikalk.com/incubator/week-picker-using-jquery-ui-datepicker */

rangepicker = {}
/* Set up the datepicker so that it selects the appropriate
 * range of dates for the timeselect. Uses sd, ed as a hack
 * so we don't have to calculate sd/ed for 'upcoming'. This
 * function is called once at page load, and then every time
 * timeselect is changed.  */
$.fn.rangepicker = function(timeselect, sd, ed, onSel) {
    /* Don't update if not needed */
    if (rangepicker.ts == timeselect)
        return false;
    rangepicker.ts = timeselect;

    var minDate, maxDate;
    if (timeselect == "upcoming") {
        rangepicker.skipAjax = true;
        rangepicker.setSdEd = function() {};
        minDate = sd;
        maxDate = ed;
    }
    else {
        minDate = null;
        maxDate = null;
        if (timeselect == "day") {
            rangepicker.setSdEd = function(date) {
                rangepicker.sd = date;
                rangepicker.ed = date;
            };
        }
        else if (timeselect == "week") {
            rangepicker.setSdEd = function(date) {
                rangepicker.sd = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 1);
                rangepicker.ed = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 7);
            };
        }
        else if (timeselect == "month") {
            rangepicker.setSdEd = function(date) {
                rangepicker.sd = new Date(date.getFullYear(), date.getMonth(), 1);
                rangepicker.ed = new Date(date.getFullYear(), date.getMonth()+1, 0);
            };
        }
    }
    rangepicker.sd = sd;
    rangepicker.ed = ed;

    /* If this isn't the first time it's been called */
    if (rangepicker.dp != undefined) {
        this.datepicker('setDate', sd);
        this.datepicker('option', 'minDate', minDate);
        this.datepicker('option', 'maxDate', maxDate);
        rangepicker.skipAjax = true;
        $(this.find('.ui-datepicker-current-day a')[0]).trigger('click');
        if (timeselect != "upcoming")
            rangepicker.skipAjax = false;
    }
    /* If this is the first time it's been called */
    else {
        rangepicker.dp = this;
        var dp = this;
        var selectDayRange = function(date) {
            var cssClass = '';
            if (date >= rangepicker.sd && date <= rangepicker.ed) {
                cssClass = 'ui-datepicker-current-day';
            }
            return [true, cssClass];
        }
        var highlightDayRange = function() {
            window.setTimeout(function () {
                dp.find('.ui-datepicker-current-day a').addClass('ui-state-active')
            }, 1);
        }
        
        dp.datepicker( {
            dateFormat: 'yymmdd',
            firstDay: 1,
            showOtherMonths: true,
            selectOtherMonths: true,
            minDate: minDate,
            maxDate: maxDate,

            onSelect: function(dateText, inst) {
                var date = $(this).datepicker('getDate');
                rangepicker.setSdEd(date);
                highlightDayRange();
                if (!rangepicker.skipAjax) onSel();
            },
            beforeShowDay: selectDayRange,
            onChangeMonthYear: function(year, month, inst) {
                highlightDayRange();
            }
        });
        highlightDayRange();

        //dp.find('.ui-datepicker-calendar tr').on('mousemove', function() { $(this).find('td a').addClass('ui-state-hover'); });
        //dp.find('.ui-datepicker-calendar tr').on('mouseleave', function() { $(this).find('td a').removeClass('ui-state-hover'); });
    }
};

