function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
    
    $('#geocode-address').on('click'), () => {
        const inputAddress = {{ full_address | tojson }};

        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({address: user}, (results, status) => {
            if (status === 'OK') {

                //Gets the coordinates of the input address
                const userLocation = results[0].geometry.location;

                //Creates a marker for the map
                const userLocationMarker = new google.maps.Marker({
                    position: userLocation,
                    map: map
                });

                //Zooms in on the geolocated location
                map.setCenter(userLocation);
                map.setZoom(20);
            }
            else {
                alert('Geocode was unsucessful for the following reason: ${status}');
            } 
        });
    });
}