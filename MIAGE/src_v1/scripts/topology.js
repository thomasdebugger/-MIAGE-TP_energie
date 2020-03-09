/// Display topology
(function(Topology){
    
    var current_visits = [];
    var current_tours = [];

    // Read visits from csv text
    Topology.readVisitsFromCsv = function(csv) {
        var data = $.csv.toArrays(csv);
        var visits = [];
        // find columns
        var id_column = -1, name_column = -1, lat_column = -1, lon_column = -1;
        for (var j = 0; j < data[0].length; j++) {
            if (data[0][j] == "visit_id") { id_column = j; }
            else if (data[0][j] == "visit_name") { name_column = j; }
            else if (data[0][j] == "visit_lat") { lat_column = j; }
            else if (data[0][j] == "visit_lon") { lon_column = j; }
        }
        if (id_column === -1 || name_column === -1 || lat_column === -1 || lon_column === -1){
            alert("Problème: Il manque une des colonnes : visit_id, visit_name, visit_lat or visit_lon");
            return;
        }

        // read each visit
        for (var i = 1; i < data.length; i++){
            var row = data[i];
            var visit = {
                id: row[id_column],
                name: row[name_column],
                lat: row[lat_column],
                lon: row[lon_column]
            };
            visits.push(visit);
        }
        current_visits = visits;
        return visits;
    }
    
    Topology.getCurrentVisits = function(){
        return current_visits;
    }

    Topology.clearCurrentVisits = function() {
        current_visits = [];
    }

    Topology.readToursFromTxt = function(txt) {
        var txt_tours = txt.split("\n");
        var tours = [];


        if (current_visits.length === 0) {
            alert("Problème: les visites doivent être fournies d'abord");
            return;
        }

        

        for (var i = 0; i < txt_tours.length; i++) {
            var text_vis_list = txt_tours[i].split(",");
            var cur_vis = [];
            cur_vis.push(current_visits[0]);
            for (var j = 0; j < text_vis_list.length; j++) {
                if (text_vis_list[j] === "R" || text_vis_list[j] === "C") {
                    text_vis_list[j] = 0; // Index in the cur_visit list
                }
                
                cur_vis.push(current_visits[text_vis_list[j]]);
            }
            cur_vis.push(current_visits[0]);
            tours.push(cur_vis);
        }

        current_tours = tours;
        return tours;
    }

    Topology.getCurrentTours = function(){
        return current_tours;
    }

    Topology.clearCurrentTours = function() {
        current_tours = [];
    }

}(window.Topology = window.Topology || {}));
