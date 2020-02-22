// get addresslist from server.py file into this javascript file
// have each address in the list iterate through the google maps geocode API converting it to a latitude and longitude coordinate
// have each lat and long for each address set as a marker
// have markers show up on map just for that 

<link rel="stylesheet" href="/static/css/styles.css"/>
<style>
    #map {
        width: 100%;
        height: 100%;
    }
</style>
{% endblock header %} 

{% block content %}

<main>
<section class="map">
<div id="map"></div>
</section>
</main>

<script>
function initMap() {
    const unitedStates = {
        lat: 37.0902,
        lng: -95.7129
    };

    const basicMap = new google.maps.Map(document.querySelector('#map'), 
                    {
                        center: unitedStates,
                        zoom: 15
                    });
}

$('#geocode-address').on('click', () => {
    const nearbyLocation = pollingAddress; 

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: nearbyLocations}, (results, status)) => {
        if (status === 'OK'( {

            <!-- Gets the coordinates of the input location -->
            const userLocation = results[0].geometry.location;

            <!-- Creates a marker -->
            const userLocationMarker = new google.maps.Marker({
                position: userLocation,
                map: map
            });

            <!-- Zoom into the geolocated location -->
            map.setCenter(userLocation);
            map.setZoom(18);
        } else {
            alert('Geocode was unsuccessful for the following reason: ${status}');
        });
    }
});
