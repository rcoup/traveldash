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
            from: td.stopfusionTableId
        }
    });
    td.stopsLayer.setMap(td.map);

    var stopId, stopName, stopLocation;
    var currentField, currentLabel;

    google.maps.event.addListener(td.stopsLayer, 'click', function(evt) {
        stopId = evt.row.id.value;
        stopName = evt.row.name.value;
        var sl = evt.row.location.value.split(' ');
        stopLocation = [parseFloat(sl[1]), parseFloat(sl[0])];

        $("#getstop-save").attr('disabled', false);
        $("#getstop-name").text(stopName);
    });

    $('#getstop-modal').modal({
        backdrop: 'static',
        keyboard: false
    }).bind('show', function() {
        $("#getstop-name").text(currentLabel.text());
        $("#getstop-save").attr('disabled', true);
        var sl = currentField.data('stopLocation');
        if (sl) {
            td.map.setZoom(14);
            td.map.setCenter(new google.maps.LatLng(sl[1], sl[0]));
        } else {
            td.map.setZoom(11);
            td.map.setCenter(new google.maps.LatLng(-36.87, 174.76));
        }
    }).bind('shown', function() {
        var z = td.map.getZoom();
        var c = td.map.getCenter();
        google.maps.event.trigger(td.map, 'resize');
        td.map.setZoom(z);
        td.map.setCenter(c);
    });
    $("#getstop-cancel").click(function(evt) {
        $("#getstop-modal").modal('hide');
    });

    $("#getstop-save").click(function(evt) {
        $("#getstop-modal").modal('hide');
        currentField.val(stopId);
        currentField.data('stopLocation', stopLocation);
        currentLabel.text(stopName);
    });

    $(".gtfsStop").hide().after(function() {
        var field = $(this);
        var container = $("<div></div>", {'class': 'mapSelect'}).text(' ');
        var label = $("<span>(None)</span>").appendTo(container);
        var button = $("<button>Select</button>").addClass('btn').click(function(evt) {
            evt.preventDefault();
            currentField = field;
            currentLabel = label;
            $('#getstop-modal').modal('show');
        }).prependTo(container);

        var m = field.attr('id').match(/id_(\w+-\d+)-(.+)/);
        var routeId = m && m[1];
        var stopInfo = m && tdStopInfo[routeId] && tdStopInfo[routeId][m[2]];
        if (stopInfo) {
            field.data('stopLocation', stopInfo.location);
            label.text(stopInfo.name);
        }
        return container;
    });
    
});
