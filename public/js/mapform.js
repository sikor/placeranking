/**
 * Created with PyCharm.
 * User: pawel
 * Date: 10.06.13
 * Time: 00:11
 * To change this template use File | Settings | File Templates.
 */




function bindMapToForm(formIds) {


    var centerLatLng = new google.maps.LatLng(50.0, 20.0);
    var mapOptions = {
        center: centerLatLng,
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    var colors = ["#00FF00", "#FF0000", "FFFF00"]

    function addMarker(latid, lonid, color, text) {
        var marker = new StyledMarker({
            styleIcon: new StyledIcon(
                StyledIconTypes.MARKER,
                {
                    color: color,
                    text: text
                }
            ),
            position: centerLatLng,
            map: map,
            draggable: true
        })

        google.maps.event.addListener(marker, 'dragend', function () {
    //            marker.setPosition(event.latLng);
            $(latid).attr("value", marker.getPosition().lat());
            $(lonid).attr("value", marker.getPosition().lng());
    //        alert(marker.getPosition().lat())
    //        alert($(latid).attr("value"))
        })

    }
    for (var i = 0; i < formIds.length; ++i) {
        var latid = "#" + formIds[i][0]
        var lonid = "#" + formIds[i][1]
//        var formMarker = new google.maps.Marker({
//            position: centerLatLng,
//            map: map
//        })
        addMarker(latid, lonid, colors[i], formIds[i][2])
    }
}