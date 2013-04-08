/* Enables range selection on the standard jQueryUI datepicker
 * Source (modified): http://www.tikalk.com/incubator/week-picker-using-jquery-ui-datepicker */

function dateStringToDate(ds) {
    return new Date(ds.substring(0,4), parseInt(ds.substring(4,6))-1, ds.substring(6,8));
}

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

rangepicker = {}
/* Set up the datepicker so that it selects the appropriate
range of dates for the timeselect. Uses sd, ed as a hack
so we don't have to calculate sd/ed for 'upcoming'. This
function is called once at page load, and then every time
timeselect is changed. */
$.fn.rangepicker = function(timeselect, sd, ed, onSel) {
    /* Don't update if not needed */
    if (rangepicker.timeselect == timeselect)
        return false;
    rangepicker.timeselect = timeselect;

    sd = dateStringToDate(sd);
    ed = dateStringToDate(ed);

    if (timeselect == "upcoming") {
        rangepicker.setSdEd = function() {};
    }
    else {
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

    /* If this isn't the first time it's been called, then we only
    need to change the timeselect and re-render the datepicker */
    if (rangepicker.dp != undefined) {
        /* Must change current date if switching to upcoming */
        if (timeselect == "upcoming")
            rangepicker.dp.datepicker('setDate', sd);
        /* Must click current date so beforeShowDay gets run */
        rangepicker.onlyAnUpdate = true;
        $(rangepicker.dp.find('.ui-datepicker-current-day a')[0]).click();
        rangepicker.onlyAnUpdate = false;
    }

    /* If this is the first time it's been called */
    else {
        rangepicker.onlyAnUpdate = false;

        this.append("<div class='rangepicker-dp'></div>");
        this.append("<div class='rangepicker-ts'></div>");
        rangepicker.dp = this.children('.rangepicker-dp');
        rangepicker.ts = this.children('.rangepicker-ts');
        rangepicker.ts.css('margin', '6px auto');
        rangepicker.ts.css('text-align', 'center');

        /* Set up timeselect tabs */
        var timeselects = ["upcoming", "day", "week", "month"];
        for (var i in timeselects) {
            var ts = timeselects[i];
            var str = '<input name="timeselect" class="evfilter-timeselect" type="radio" id="'+ts+'"';
            if (timeselect == ts)
                str += ' checked="checked"';
            str += ' /><label for="'+ts+'">'+ts.capitalize()+'</label>';
            rangepicker.ts.append(str);
        }
        rangepicker.ts.buttonsetsq();
        rangepicker.ts.find('input').click(function(ev) {
            if (rangepicker.onlyAnUpdate) return;
            onSel();
        });

        /* Set up prev+next buttons */
        /* TODO */

        var selectDayRange = function(date) {
            var cssClass = '';
            if (date >= rangepicker.sd && date <= rangepicker.ed) {
                cssClass = 'ui-datepicker-selected';
            }
            return [true, cssClass];
        };
        var highlightDayRange = function() {
            window.setTimeout(function () {
                rangepicker.dp.find('.ui-datepicker-selected a').addClass('ui-state-active')
            }, 1);
        };
        var updateDatepicker = function(date) {
            if (rangepicker.onlyAnUpdate) {
                highlightDayRange();
                return false;
            }

            if (rangepicker.timeselect != 'upcoming' && (date < rangepicker.sd || date > rangepicker.ed)) {
                rangepicker.setSdEd(date);
                highlightDayRange();
                return true;
            }
            /* We must click to update, setting checked=true doesn't work for some reason... */
            rangepicker.onlyAnUpdate = true;
            $('#day').click();
            rangepicker.onlyAnUpdate = false;
            return true;
        };
        
        rangepicker.dp.datepicker( {
            dateFormat: 'yymmdd',
            firstDay: 1,
            changeMonth: true,
            changeYear: true,
            showOtherMonths: true,
            selectOtherMonths: true,

            beforeShowDay: selectDayRange,
            onSelect: function(dateText, inst) {
                var date = $(this).datepicker('getDate');
                if (updateDatepicker(date)) onSel();
            },
            onChangeMonthYear: function(year, month, inst) {
                highlightDayRange();
            }
        });
        highlightDayRange();

        //dp.find('.ui-datepicker-calendar tr').on('mousemove', function() { $(this).find('td a').addClass('ui-state-hover'); });
        //dp.find('.ui-datepicker-calendar tr').on('mouseleave', function() { $(this).find('td a').removeClass('ui-state-hover'); });
    }
};

