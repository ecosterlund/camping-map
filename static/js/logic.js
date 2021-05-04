// An empty array of camps and their locations built for the api call.  Format should look like the below when populated
//   {
//   name: "Nantes",
//   location: [47.2184, -1.5536]
//   }
var camps = [];
var parks = [];
// An array which will be used to store created camp markers
var campMarkers = L.markerClusterGroup();
var parkMarkers = L.markerClusterGroup();

var parkIcon = L.Icon.extend({
  options: {
      iconSize:     [32, 37],
      iconAnchor:   [16, 37],
      popupAnchor:  [0, -45]
  }
});
var realParkIcon = new parkIcon({iconUrl: 'static/icons/riparianhabitat.png'})

var campIcon = L.Icon.extend({
  options: {
      iconSize:     [32, 37],
      iconAnchor:   [16, 37],
      popupAnchor:  [0, -45]
  }
});
var realCampIcon = new campIcon({iconUrl: 'static/icons/wildderness_camping.png'})



// @TODO If we have extra time, change cluster colors
// function clusterMaker(cluster) {
//   var markers = cluster.getAllChildMarkers();
//   var n = 0;
//   for (var i = 0; i < markers.length; i++) {
//     n += markers[i].number;
//   }
//   var small = n < 65;
//   var className = small ? 'mycluster1' : 'mycluster2';
//   var size = small ? 40 : 60;
//   return L.divIcon({ html: n, className: className, iconSize: L.point(size, size) });
// }







// Testing objects, here for posterity
// var tcg1 = {
//   "name": "277 North Campground",
//   "location": [29.51187, -100.907479]
// };
// var tcg2 = {
//   "name": "Adirondack Shelters",
//   "location": [39.677404, -77.48308]
// };
// var test = [tcg1, tcg2];



// URL for parks dept api, adds api key stored in config.js
var campsURL = "https://developer.nps.gov/api/v1/campgrounds?limit=1000&api_key=" + PARKS_KEY;
var parksURL = "https://developer.nps.gov/api/v1/parks?limit=1000&api_key=" + PARKS_KEY;

d3.json(parksURL).then((p_response) => {

  for (var i = 0; i < p_response.data.length; i++) {
    
    if (p_response.data[i].latitude != ""){
      var p_lat = parseFloat(p_response.data[i].latitude);
      var p_lng = parseFloat(p_response.data[i].longitude);
      var p_description = p_response.data[i].description
      var designation = p_response.data[i].designation
      var pUrl = p_response.data[i].url
      if (pUrl = ""){
        pURL = "https://www.nps.gov/planyourvisit/index.htm"
      }
      var p_name = p_response.data[i].fullName;
      var p_location = [p_lat, p_lng]
      var p_obj = {
        name: p_name,
        location: p_location,
        description: p_description,
        designation: designation,
        pUrl: pUrl
      }
      parks.push(p_obj) 
    } else {
      continue;
    }
  };


  for (var i = 0; i < parks.length; i++) {
    // loop through the parks array, create a new marker, push it to the camps markers array
    parkMarkers.addLayer(
      L.marker(parks[i].location, {icon: realParkIcon})
      .bindPopup("<h2>" + parks[i].name + "</h2><h3>" + parks[i].designation + "</h3><p>" + parks[i].description + `</p><a href=${parks[i].pUrl} target="_blank">` + "Click Here to Plan Your Visit" +"</a>")
    );
    
  }


                  // Feeding the api url into d3 and getting the JSON as a response
                  d3.json(campsURL).then((response) => {
                    
                    
                    

                    // For loop to run the length of data in the response
                    for (var i = 0; i < response.data.length; i++) {

                          // Some camps do not have a lat lng listed, so we only want to append our camps list with camps who's lat lng are listed.  If they do not have a value the loop continues
                          if (response.data[i].latitude != ""){
                            var lat = parseFloat(response.data[i].latitude);
                            var lng = parseFloat(response.data[i].longitude);
                            var description = response.data[i].description
                            var reservationInfo = response.data[i].reservationInfo
                            var reservationUrl = response.data[i].reservationUrl
                            if (reservationUrl = ""){
                              reservationUrl = "https://www.nps.gov/planyourvisit/index.htm"
                            }
                            var name = response.data[i].name;
                            var location = [lat, lng]
                            var obj = {
                              name: name,
                              location: location,
                              description: description,
                              reservationInfo: reservationInfo,
                              reservationUrl: reservationUrl
                            }
                            camps.push(obj) 
                            

                          } else {
                              continue;
                            }
                    };




                  for (var i = 0; i < camps.length; i++) {
                    // loop through the camps array, create a new marker, push it to the camps markers array
                    campMarkers.addLayer(
                      L.marker(camps[i].location, {icon: realCampIcon})
                      .bindPopup("<h2>" + camps[i].name + "</h2><p>" + camps[i].description + "</p><h3>" + camps[i].reservationInfo + `</h3><a href=${camps[i].reservationUrl} target="_blank">` + "Click Here to Plan Your Visit" + "</a>")
                    );
                    
                  }


                  // Add all the camp Markers to a new layer group.
                  // Now we can handle them as one group instead of referencing each individually
                  var campLayer = L.layerGroup(campMarkers);
                  var parkLayer = L.layerGroup(parkMarkers);


                  // Define variables for our tile layers
                  var outdoors = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
                    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
                    maxZoom: 18,
                    id: "outdoors-v11",                    
                    // id: "light-v10",
                    accessToken: API_KEY
                  });

                  var dark = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
                    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
                    maxZoom: 18,
                    id: "dark-v10",
                    accessToken: API_KEY
                  });

                  // Only one base layer can be shown at a time
                  var baseMaps = {
                    Outdoors: outdoors,
                    Dark: dark
                  };

                  // Overlays that may be toggled on or off
                  var overlayMaps = {
                    Parks: parkMarkers,
                    Campgrounds: campMarkers
                  };

                  // Create map object and set defaults, lat/long for center of america
                  var myMap = L.map("map", {
                    center: [44.967243, -103.771556], 
                    zoom: 4,
                    layers: [outdoors, parkMarkers, campMarkers] 
                  });

                  // Pass our map layers into our layer control
                  // Add the layer control to the map
                  L.control.layers(baseMaps, overlayMaps).addTo(myMap);

                  

                  })
                // --------------------------- PUT HEAT MAP CODE HERE------------------------------------------------------
                
                // d3.json(dat)



                // d3.json(url).then(function(response) {
                
                //   console.log(response);
                
                //   var heatArray = [];
                
                //   for (var i = 0; i < response.length; i++) {
                //     var location = response[i].location;
                
                //     if (location) {
                //       heatArray.push([location.coordinates[1], location.coordinates[0]]);
                //     }
                //   }
                
                //   var heat = L.heatLayer(heatArray, {
                //     radius: 20,
                //     blur: 35
                //   }).addTo(myMap);
                
                // });
                // ----------------------- END OF HEATMAP EXAMPLE CODE--------------------------------
})                  // everything must be in the d3 call, or async will not populate parks before using it to populate parkMarkers