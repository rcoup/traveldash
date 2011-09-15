window.td = window.td || {};

$(function() {
    td.map = new google.maps.Map($("#map")[0], {
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: new google.maps.LatLng(-36.87, 174.76)
    });
    
    td.stopsLayer = new google.maps.FusionTablesLayer({
        query: {
            select: 'location',
            from: '1489165'
        }
    });
    td.stopsLayer.setMap(td.map);

    $("#map").hide();

    var activeButton;
    $(".gtfsStop").hide().after(function() {
        var field = $(this);
        console.log(field[0].id);
        var gmapsEvt;
        var container = $("<div></div>", {'class': 'mapSelect'}).text(' ');
        var label = $("<span>(None)</span>").appendTo(container);
        var button = $("<button>Select</button>").toggle(
            function() {
                if (activeButton) {
                    activeButton.trigger('click');
                }
                
                gmapsEvt = google.maps.event.addListener(td.stopsLayer, 'click', function(evt) {
                    field.val(evt.row.id.value);
                    label.text(evt.row.name.value);
                    button.text("Save");
                });
                $("#map").show();
                google.maps.event.trigger(td.map, 'resize');
                $(this).text("Cancel");
                activeButton = $(this);
            },
            function() {
                $("#map").hide();
                google.maps.event.removeListener(gmapsEvt);
                $(this).text("Select");
                activeButton = null;
            }
        ).prependTo(container);
        return container;
    });
    
});
