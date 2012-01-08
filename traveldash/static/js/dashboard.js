
(function() {
    window.td = {
        warning_time: 0,

        formatDateUntil : function(date) {
            var delta = -date.getElapsed();
            var h = Math.floor(delta / (60*60*1000));
            var m = Math.ceil((delta - h*(60*60*1000)) / (60*1000));
            
            var s = m + " mins";
            if (h) {
                s = h + " hr " + s;
            }
            return s;
        },
        
        makerow: function(dep, route) {
            var trip = dep.trip;
            var departs = Date.parse(dep.departs);
            var arrives = Date.parse(dep.arrives);
            var endTime = arrives.clone().addMinutes(route.to.walk_time);

            var row = $("<tr/>", {
                    id: "td_trip_" + trip.id,
                    "class": "dep"
                })
                .data('departure', dep);
            
            $("<th/>", {
                "class": "mode routeType" + trip.mode
                })
                .appendTo(row)
                .append($("<abbr/>", {
                    title: route.name,
                    html: "&nbsp;"
                }));

            $("<th/>", {
                "class": "code",
                text: trip.short_name
                })
                .appendTo(row);
            
            $("<td/>", {
                "class": "name",
                text: trip.long_name
                })
                .appendTo(row);
            
            var z = $("<td/>", {
                "class": "departs"
                })
                .appendTo(row)
                .append($("<span/>", {
                    "class": "departsETA tooltip",
                    text: td.formatDateUntil(departs),
                    title: "departs at " + departs.toString("t") + " from " + route.from.name
                }));
            
            $("<td/>", {
                "class": "arrives"
                })
                .appendTo(row)
                .append($("<span/>", {
                    "class": "tooltip",
                    text: endTime.toString("t"),
                    title: "arrives at " + arrives.toString("t") + " at " + route.to.name
                }));
            return row;
        },
        
        update: function() {
            $.getJSON('data/', function(data) {
                td.warning_time = data.warning_time;

                var valid_ids = [];
                $.each(data.departures, function(i, dep) {
                    var id = "td_trip_" + dep.trip.id;
                    if (!$("#" + id).length) {
                        var route = data.routes[dep.route];
                        td.schedule.append(td.makerow(dep, route));
                    }
                    valid_ids.push(id);
                });
                $("tr", td.schedule)
                    .filter(function(i) {
                        return (valid_ids.indexOf(this.id) < 0);
                    })
                    .remove();
                td.refreshTimes();
            });
        },

        refreshTimes : function() {
            $('.dep').each(function(i) {
                var dep = $(this).data('departure');
                var departs = Date.parse(dep.departs);
                var deltaMins = -departs.getElapsed() / (60*1000);
                if (deltaMins < dep.walk_time_start) {
                    $(this).remove();
                } else {
                    $(".departsETA", this).text(td.formatDateUntil(departs));

                    if (Math.ceil(deltaMins) <= td.warning_time) {
                        $(this).toggleClass("warning", true);
                    }
                }
            });
        }
    };

    $(function() {
        // times in seconds
        var UPDATE = 5*60;
        var REFRESH = 20;

        if (Modernizr.touch) {
            // for touch devices, use click to activate and clear tooltips
            $('#schedule').delegate('.tooltip', 'click', function () {
                var tw = $(this).data('twipsy');
                if (!tw) {
                    $(this).twipsy({placement: 'below', trigger: 'manual'});
                }
                $(this).twipsy('toggle');
            });
            $('body').delegate('.twipsy', 'click', function () {
                var $tip = $(this);
                $tip.removeClass('in');

                function removeElement() {
                    $tip.remove();
                }
                var transitionEnd;
                if ($.support.transition) {
                    transitionEnd = "TransitionEnd";
                    if ($.browser.webkit) {
                        transitionEnd = "webkitTransitionEnd";
                    } else if ($.browser.mozilla) {
                        transitionEnd = "transitionend";
                    } else if ($.browser.opera) {
                        transitionEnd = "oTransitionEnd";
                    }
                }

                if ($.support.transition && $tip.hasClass('fade')) {
                    $tip.bind(transitionEnd, removeElement);
                } else {
                    removeElement();
                }
            });
        } else {
            $('#schedule .tooltip').twipsy({live: true, placement: 'below'});
        }

        // onload
        td.schedule = $("#schedule");
        td.update();

        window.setInterval(td.update, UPDATE*1000);
        window.setInterval(td.refreshTimes, REFRESH*1000);

        window.addEventListener('focus', function() {
            td.refreshTimes();
            td.update();
        });
    });
})();
