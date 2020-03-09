/// Get parameters filled by user
(function(Parameters){    

    // Detect the start time format and return it in seconds
    // Ex:  if 28800, return 28800
    //      if 8:00:00 or 08:00:00 or 8:00, return 28800
    function getStartTimeInSeconds(start_time) {
        var pieces = start_time.split(':');
        if (pieces.length == 2) {
            hour = parseInt(pieces[0], 10);
            minute = parseInt(pieces[1], 10);
            return 60 * minute + 3600 * hour;
        }
        if (pieces.length == 3) {
            hour = parseInt(pieces[0], 10);
            minute = parseInt(pieces[1], 10);
            second = parseInt(pieces[2], 10);
            return second + 60 * minute + 3600 * hour;
        }

        return start_time;
    }

    // Get all parameters filled by user for tour request
    Parameters.getAllParameters = function(){
        // get coordinates
        // var origin_latitude = document.getElementById('origin_latitude').value,
        // origin_longitude = document.getElementById('origin_longitude').value,

        var loading_profile = "0";
        var idx = loading_profile_list.selectedIndex;
        loading_profile = loading_profile_list.options[idx].value;  

        var single_search = document.getElementById('single_search').checked;

        // TODO
        return {
            origin_latitude : origin_latitude,
            origin_longitude: origin_longitude,
            destination_latitude: destination_latitude,
            destination_longitude: destination_longitude,
            start_profile: start_profile,
            arrival_profile: arrival_profile,
            first_path_max_radius: first_path_max_radius,
            last_path_max_radius: last_path_max_radius,
            day_of_week: day_of_week,
            start_time: start_time,
            duration: duration,
            no_bus: no_bus,
            no_tram: no_tram,
            no_train: no_train,
            no_subway: no_subway,
            max_transfer_time: max_transfer_time,
            transfer_speed_level: transfer_speed_level,
            single_search: single_search
        };
    };

    // TODO
    // Fill URL for tour with parameters (sent by Parameters.getAllParameters)
    Parameters.getUrlForTourGenerationRequest = function(serverUri, params){
        var callUri = serverUri + "?dayofweek="+ params.day_of_week +"&seconds=" + params.start_time 
            + "&from_lat=" + params.origin_latitude + "&from_lng=" + params.origin_longitude
            + "&to_lat=" + params.destination_latitude + "&to_lng=" + params.destination_longitude
            + "&first_path_mode=" + params.start_profile + "&last_path_mode=" + params.arrival_profile ;

        if (params.duration && params.duration != "") {
            callUri += "&duration=" + params.duration;
            // TODO : remove when bug fixed
            callUri += "&rewrite=false";
        }

        if (params.first_path_max_radius && params.first_path_max_radius != "" && params.first_path_max_radius != "Default") {
            callUri += "&first_path_max_radius=" + params.first_path_max_radius;
        }
        if (params.last_path_max_radius && params.last_path_max_radius != "" && params.last_path_max_radius != "Default") {
            callUri += "&last_path_max_radius=" + params.last_path_max_radius;
        }
        if (params.single_search){
            callUri += "&single_search=true";
        }
        if (params.no_bus){
            callUri += "&no_bus=true";
        }
        if (params.no_tram){
            callUri += "&no_tram=true";
        }
        if (params.no_train){
            callUri += "&no_train=true";
        }
        if (params.no_subway){
            callUri += "&no_subway=true";
        }

        if (params.max_transfer_time && params.max_transfer_time != "") {
            callUri += "&max_transfer_time=" + params.max_transfer_time;
        }
        callUri += "&transfer_speed_level=" + params.transfer_speed_level;

        return callUri
    };

    function compute_direct_distance(lat1, lon1, lat2, lon2) {
        var radlat1 = Math.PI * lat1/180
        var radlat2 = Math.PI * lat2/180
        var theta = lon1-lon2
        var radtheta = Math.PI * theta/180
        var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
        dist = Math.acos(dist) * 6371000;
        return Math.round(dist);
    }

    Parameters.computeAndSetDirectDistance = function(){
        // get coordinates
        var origin_latitude = document.getElementById('origin_latitude').value,
        origin_longitude = document.getElementById('origin_longitude').value,
        destination_latitude = document.getElementById('destination_latitude').value,
        destination_longitude = document.getElementById('destination_longitude').value;
        var distance = compute_direct_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude);
        document.getElementById('direct_distance').textContent  = distance + " m";
    }

    Parameters.computeDirectDistance = function(){
        // get coordinates
        var origin_latitude = document.getElementById('origin_latitude').value,
        origin_longitude = document.getElementById('origin_longitude').value,
        destination_latitude = document.getElementById('destination_latitude').value,
        destination_longitude = document.getElementById('destination_longitude').value;
        var distance = compute_direct_distance(origin_latitude, origin_longitude, destination_latitude, destination_longitude);
        return distance;
    }

    Parameters.computeDistance = function(lat1,lon1,lat2,lon2) {
        return compute_direct_distance(lat1,lon1,lat2,lon2);
    }

    // Returns Origin coordinates as [lat, lon]
    Parameters.getOriginLatLong = function(){
        return [document.getElementById('origin_latitude').value, document.getElementById('origin_longitude').value];
    }
    // Returns Destination coordinates as [lat, lon]
    Parameters.getDestinationLatLong = function(){
        return [document.getElementById('destination_latitude').value, document.getElementById('destination_longitude').value];
    }

    Parameters.setOriginLatLong = function(latitude, longitude){
        document.getElementById('origin_latitude').value = latitude;
		document.getElementById('origin_longitude').value = longitude;
    }
    
    Parameters.setDestinationLatLong = function(latitude, longitude){
        document.getElementById('destination_latitude').value = latitude;
		document.getElementById('destination_longitude').value = longitude;
    }

    Parameters.getODPartition = function(){
        return document.getElementById('od_partition').value;
    }

    Parameters.getStopsMaxDistance = function(){
        return document.getElementById('stop_distance').value;
    }

    Parameters.getStopsEllipseRatio = function(){
        return document.getElementById('stop_ellipse_ratio').value;
    }

    // 0 for origin, 1 for destination
    Parameters.getOdPartitionCenter = function(){
        var idx = od_partition_center.selectedIndex;
        var center = od_partition_center.options[idx].value;  
        return center;
    }
    // 0 for origin, 1 for destination
    Parameters.getStopDistanceCenter = function(){
        var idx = stop_distance_center.selectedIndex;
        var center = stop_distance_center.options[idx].value;  
        return center;
    }

    // Returns Rectangle bottom left coordinates as [lat, lon]
    Parameters.getRectangleBottomLeftLatLong = function(){
        return [document.getElementById('bottom_left_latitude').value, document.getElementById('bottom_left_longitude').value];
    }
    // Returns Rectangle top right coordinates as [lat, lon]
    Parameters.getRectangleTopRightLatLong = function(){
        return [document.getElementById('top_right_latitude').value, document.getElementById('top_right_longitude').value];
    }

    Parameters.getTourServerUri = function(){
        return document.getElementById('tour_server').value;
    }

}(window.Parameters = window.Parameters || {}));
