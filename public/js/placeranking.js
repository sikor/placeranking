function initialize() {
    var centerLatLng = new google.maps.LatLng(50.0, 20.0);
    var mapOptions = {
        center: centerLatLng,
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);


    $.ajax({
        url: "/rest/opinion",
        cache: false,
        dataType: "json"
    }).done( function(jsonOpinions){
            $.each(jsonOpinions, function(index, opinion){
                var latlngArr = opinion.location.split(",");
                var position = new google.maps.LatLng(latlngArr[0], latlngArr[1])
                var marker = new google.maps.Marker({
                            position: position,
                            map: map,
                            title: opinion.comment
                     });
                var infowindow = new google.maps.InfoWindow();
                google.maps.event.addListener(marker, 'click', function(){
                    infowindow.setContent(opinion.comment);
                    infowindow.open(map, marker)
                })
            })
        });


    var formMarker = new google.maps.Marker({
        position:centerLatLng,
        map:map
    })

    google.maps.event.addListener(map, 'click', function(event){
        formMarker.setPosition(event.latLng);
        $("#lati").attr("value", event.latLng.lat());
        $("#long").attr("value", event.latLng.lng());
    })
}

google.maps.event.addDomListener(window, 'load', initialize);
