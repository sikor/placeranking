function initialize() {
    var centerLatLng = new google.maps.LatLng(50.0, 20.0);
    var mapOptions = {
        center: centerLatLng,
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);


    var markerVisualization = function (opinion, position) {
        var marker = new google.maps.Marker({
            position: position,
            map: map,
            title: opinion.comment
        });

        return marker
    }

    var styleMarkerVisualization = function (opinion, position) {
        var color;
        if (opinion.sentiment == "Positive")
            color = "#00FF00";
        else if (opinion.sentiment == "Negative")
            color = "#FF0000";
        else
            color = "FFFF00";

        var marker = new StyledMarker({
            styleIcon: new StyledIcon(
                StyledIconTypes.MARKER,
                {
                    color: color
                }
            ),
            position: position,
            map: map
        });
        return marker
    }
    var circleVisualization = function (opinion, position) {
        var opinionOptions = {
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: position,
            radius: 30
        };
        var opinionCircle = new google.maps.Circle(opinionOptions);
        return opinionCircle
    }

    var infoWindowListener = function (opinion, marker) {
        var infowindow = new google.maps.InfoWindow();
        google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(opinion.comment);
            infowindow.open(map, marker)
        })
    }


    var visualizationEngine = styleMarkerVisualization
    var listenerEngine = infoWindowListener


    $.ajax({
        url: "/rest/opinion",
        cache: true,
        dataType: "json"
    }).done(function (jsonOpinions) {
            $.each(jsonOpinions, function (index, opinion) {
                var latlngArr = opinion.location.split(",");
                var position = new google.maps.LatLng(latlngArr[0], latlngArr[1])
                var obj = visualizationEngine(opinion, position)
                listenerEngine(opinion, obj)
            })
        });


    var formMarker = new google.maps.Marker({
        position: centerLatLng,
        map: map
    })

    google.maps.event.addListener(map, 'click', function (event) {
        formMarker.setPosition(event.latLng);
        $("#lati").attr("value", event.latLng.lat());
        $("#long").attr("value", event.latLng.lng());
    })
}

google.maps.event.addDomListener(window, 'load', initialize);
