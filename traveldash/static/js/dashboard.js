
(function() {
    window.td = {
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

            var row = $("<tr/>", {id: "td_trip_" + trip.id});
            
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
                .append($("<abbr/>", {
                    text: td.formatDateUntil(departs),
                    title: "departs at " + departs.toString("t") + " from " + route.from.name
                }));
            console.log(z);
            
            $("<td/>", {
                "class": "arrives"
                })
                .appendTo(row)
                .append($("<abbr/>", {
                    text: endTime.toString("t"),
                    title: "arrives at " + arrives.toString("t") + " at " + route.to.name
                }));
            return row;
        },
        
        update: function() {
            $.getJSON('data/', function(data) {
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
                $.touchTooltip();
            });
        }
    };

    $(function() {
        // onload
        td.schedule = $("#schedule");
        td.update();
        window.setInterval(td.update, 60000);
    });
})();