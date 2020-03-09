/// Main code : deals with map and tour requests
(function (window) {
    'use strict';

	var L, map, layerControl, osm_layer, visitLayer, tourLayer, arrowLayer,
		currentLayers = [],
		origin_marker = null, destination_marker = null,
		serverUri = "http://127.0.0.1:23000/path";

	// Default coordinates for Lyon
	var defaultViewLatitude = 45.755308, 
		defaultViewLongitude = 4.853897,
		defaultOriginLatitude = 45.762613,
		defaultOriginLongitude = 4.813728,
		defaultDestLatitude = 45.76008,
		defaultDestLongitude = 4.86274,
		defaultZoom = 13;

	// check global value from remote_server.js or from current URL if it's deployed
	if (tourServerUri && tourServerUri !== ""){
		serverUri = tourServerUri + "/path";
	}
	if (window.location.hostname != "") {
		serverUri = window.location.origin + "/path";
	}

	// Update uri from value entered by user
	function modifyTourUri(){
		serverUri = Parameters.getTourServerUri() + "/path";
	}
	
	// Call server to get tours
	function callTourGeneration(){
		disableButtons();
		clearAll();

		var parameters = Parameters.getAllParameters();
		var callUri =  Parameters.getUrlForTourGenerationRequest(serverUri, parameters);
		$.get(callUri, handleTourResult)
		.fail(function(xhr, status, error) {clearAll()
			$("#displayedMessage").html('<span class="message_error">Error when trying to call server.</span>');
			enableButtons();
		});
	}

	// Function called when server send result for itinerary request
	// --> display result on map and description beneath
	function handleTourResult(data, status)
	{
		displayTravelsOnMap(data.travels);

		TravelDescription.displayTravelDescription(data.travels);

		enableButtons();
	}

	function displayTravelsOnMap(travels)
	{
		var travel_count = 0;
		var trips_count = 0;
		travels.forEach(travel => {
			travel_count +=1;
			travel.trips.forEach(trip => {
				if (trip.other_mode_path) {
					trips_count += displayModePath(trip, travel_count);
				}
				else{
					trips_count += displayPublicTransportPath(trip, travel_count);
				}
			});
		});

		// specific case when no result found
		if (trips_count === 0) return;

		// zoom on first travel
		var bounds = currentLayers[0][0].getBounds();
		currentLayers[0].forEach(layer => {
			bounds.extend(layer.getBounds());
		});
		map.fitBounds(bounds);
	}

	function displayModePath(trip, travel_count){
		var color = "#5522ff";
		var path_mode = "Walk"
		if (trip.other_mode && trip.other_mode == 1)
		{
			color = "#55ff55";
			path_mode = "Bike";
		}
		else if (trip.other_mode && (trip.other_mode == 2 || trip.other_mode == 3))
		{
			color = "#ff2222";
			path_mode = "Car";
		}

		var coordinates = [];
		var duration = "?";
		if (trip.other_mode_path.routes) {
			// Result from OSRM
			var route = trip.other_mode_path.routes[0]; 
			duration = route.duration;
			if (route.geometry && route.geometry.coordinates) {
				coordinates = route.geometry.coordinates;
			}
			else
			{
				trip.other_mode_path.waypoints.forEach(waypoint => {
					coordinates.push(waypoint.location);
				});
			}
		}
		else if (trip.other_mode_path.from_lng) {
			// Result from ModePathProviderCrowFlies
			coordinates.push([trip.other_mode_path.from_lng, trip.other_mode_path.from_lat]);
			coordinates.push([trip.other_mode_path.to_lng, trip.other_mode_path.to_lat]);

		}
		var newLayer = L.geoJson(null, {
			style: function (feature) {
					return { color: color };
			},
			onEachFeature: onEachFeature
		});
		var feature = { "type": "Feature", 
						"geometry": {"coordinates": coordinates, 
									"type": "LineString"},
						"properties": { "name": path_mode + " (" + Math.round(duration) + " s)" } 
					};
		newLayer.addData(feature);

		var layer_name = "<span style='color: " + color + "'> T" + travel_count + " " + path_mode + "</span>";

		layerControl.addOverlay(newLayer, layer_name, "Travel "+ travel_count);
		if (travel_count == 1) map.addLayer(newLayer);

		if (!currentLayers[travel_count-1]) currentLayers[travel_count-1] = [];
		currentLayers[travel_count-1].push(newLayer);

		return 1;
	}

	function displayPublicTransportPath(trip, travel_count){
		var color = "#222222";
		var start_seconds = 0, arrival_seconds = 0;
		
		if (trip.steps.length > 0){
			start_seconds = trip.steps[0].seconds;
			arrival_seconds = trip.steps[trip.steps.length-1].seconds;
		}
		else return 0;
		
		var newLayer = L.geoJson(null, {
			style: function (feature) {
					return { color: color };
			},
			onEachFeature: onEachFeature
		});

		var coordinates = [];
		trip.steps.forEach(step => {
			coordinates.push([step.loc.lng, step.loc.lat]);
		});
		var feature = { "type": "Feature", 
						"geometry": {"coordinates": coordinates, 
									"type": "LineString"},
						"properties": { "name": "Route " + trip.route_name + ", from " + start_seconds + " to " + arrival_seconds + " s" } 
					};
		newLayer.addData(feature);

		var layer_name = "<span style='color: " + color + "'> T" + travel_count + " " + trip.route_name + "</span>";

		layerControl.addOverlay(newLayer, layer_name, "Travel "+ travel_count);
		if (travel_count == 1) map.addLayer(newLayer);
		
		if (!currentLayers[travel_count-1]) currentLayers[travel_count-1] = [];
		currentLayers[travel_count-1].push(newLayer);

		return 1;
	}

	function disableButtons(){
		$('.action_button').prop('disabled', true);
	}

	function enableButtons(){
		$('.action_button').prop('disabled', false);
	}

	// clear all layers and results descriptions
	function clearAll() {			
		currentLayers.forEach(layers => 
			{ layers.forEach(layer => {
				map.removeLayer(layer);
			});
		});
		currentLayers = [];

		clearVisitsLayer();

		layerControl.remove();
		layerControl = new L.control.groupedLayers(
            { 'osm tiles': osm_layer }, 
            { }, 
			{ groupCheckboxes: true }
		).addTo(map);
		
		TravelDescription.clearAll();
	}

	// display popup when click on the element
	function onEachFeature(feature, layer) {
		var toDisplay = "";
		if (feature.properties) {
			if (feature.properties.name){
				toDisplay += feature.properties.name;
			}
			else if (feature.properties.Name){
				toDisplay += feature.properties.Name;
			}
		}

		if (!toDisplay){
			toDisplay = "No data";
		}

		layer.bindPopup(toDisplay);
	}


	// Load visits from input file
	function loadVisits() {
		$("#message_for_visits").text("");
		Topology.clearCurrentVisits();
		clearVisitLayer();

		var fileList = this.files;
		if (fileList.length === 0) return;

		var file = fileList[0];
		var reader = new FileReader();
		reader.readAsText(file);
		reader.onload = function(event){
			var visits = Topology.readVisitsFromCsv (event.target.result);
			if (visits.length === 0){
				$("#message_for_visits").text("No visits found in the file");
			}
			else {
				$("#message_for_visits").text((visits.length - 1) + " visits found in the file");
			}
		};
		reader.onerror = function(){ alert('Unable to read ' + file.fileName); };
	}

	// Show all loaded visits
	function showAllVisits(){
		var visits = Topology.getCurrentVisits();
		if (visits === null || visits.length === 0) {
			$("#message_for_visits").text("Please load a visit file.");
			return;
		}
		displayVisits(visits);
	}

	// Display visits on map
	// visits: array of {id, name, lat, lon}
	function displayVisits(visits){
        var is_depot = true;
		visits.forEach(visit => {
            if (is_depot) {
			    var visit_marker = L.marker(L.latLng(visit.lat, visit.lon), {
				    title: visit.name + " (" + visit.id + ")",
				    icon: L.icon({ iconUrl: './css/images/marker-depot-icon-2x.png',
								    iconSize: [12, 34],
								    iconAnchor: [6, 17],
							    })
				    });
				visit_marker.addTo(visitLayer);
                is_depot = false;
            } else {
			    var visit_marker = L.marker(L.latLng(visit.lat, visit.lon), {
				    title: visit.name + " (" + visit.id + ")",
				    icon: L.icon({ iconUrl: './css/images/marker-visit-icon-2x.png',
								    iconSize: [12, 34],
								    iconAnchor: [6, 17],
							    })
				    });
				visit_marker.addTo(visitLayer);
            }
		});
	}

	function clearVisitLayer() {
		visitLayer.clearLayers();
	}


	// Load visits from input file
	function loadTours() {
		$("#message_for_tours").text("");
		Topology.clearCurrentTours();
		clearTourLayer();

		var fileList = this.files;
		if (fileList.length === 0) return;

		var file = fileList[0];
		var reader = new FileReader();
		reader.readAsText(file);
		reader.onload = function(event){
			var tours = Topology.readToursFromTxt (event.target.result);
			if (tours.length === 0){
				$("#message_for_tours").text("No tours found in the file");
			}
			else {
				$("#message_for_tours").text((tours.length - 1) + " tours found in the file");
			}
		};
		reader.onerror = function(){ alert('Unable to read ' + file.fileName); };
	}

	// Show all loaded tours
	function showAllTours(){
		var tours = Topology.getCurrentTours();
		if (tours === null || tours.length === 0) {
			$("#message_for_tours").text("Please load a tour file.");
			return;
		}
		displayTours(tours);
	}

	// Display tours on map as polyligns
	// tours are arrays of visits (array of {id, name, lat, lon})
	function displayTours(tours){

        var colors = ['red', 'blue', 'green', 'orange', 'yellow', 'black', 'white'];
        for (var i = 0; i < tours.length; i++) {
            var latlngs = [];
            var tour = tours[i];
            for (var j = 0; j < tour.length; j++) {
                latlngs.push([tour[j].lat, tour[j].lon]);
            }
            var polyline = L.polyline(latlngs, {color: colors[i]}).addTo(tourLayer);
            
        }

	}

	function clearTourLayer() {
		tourLayer.clearLayers();
	}
    

    function initMap() {
        L = window.L;
        map = L.map('mapid').setView([defaultViewLatitude, defaultViewLongitude], defaultZoom);
        osm_layer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 23,
            maxNativeZoom: 18
            });
        osm_layer.addTo(map);

        // display list of loaded layers
		layerControl = new L.control.groupedLayers(
            { 'osm tiles': osm_layer }, 
            { }, 
			//{ position: 'topleft', collapsed: false, groupCheckboxes: true }
			{ groupCheckboxes: true }
		).addTo(map);


		// visit layer
		visitLayer = L.layerGroup().addTo(map);
        // visitLayer = L.markerClusterGroup({maxClusterRadius: 50}).addTo(map);
        // tour layer
        tourLayer = L.layerGroup().addTo(map);
		
		document.getElementById('call_tours').onclick = callTourGeneration;
		document.getElementById('clear_all').onclick = clearAll;
		document.getElementById('load_visits').onchange = loadVisits;
		document.getElementById('show_all_visits').onclick = showAllVisits;
		document.getElementById('clear_visits').onclick = clearVisitLayer;
		document.getElementById('load_tours').onchange = loadTours;
		document.getElementById('show_all_tours').onclick = showAllTours;
		document.getElementById('clear_tours').onclick = clearTourLayer;
		document.getElementById('modify_tours_uri').onclick = modifyTourUri;
	
		$(document).on({
			ajaxStart: function() { $('.message').addClass("loading"); },
			ajaxStop: function() { $('.message').removeClass("loading"); }
		});
    }

    window.addEventListener('load', function () {
        initMap();
    });
}(window));
