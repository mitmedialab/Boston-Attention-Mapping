$(document).ready(function() {
              
               if (location.href.indexOf("file:///") >= 0){
                  window.couchURL = 'http://127.0.0.1:5984/';
                } else{
                  window.couchURL = 'couchdb/';
                }
                showMetadata();

                window.mapCenter = new google.maps.LatLng(42.358056, -71.063611);

                $("#enter-button").click(function(e){
                    $("#loading-screen").fadeOut('slow');
                    $("#h1-title").fadeIn('slow');
                    e.preventDefault();
                });
                $("#about-button").click(function(e){
                    $("#loading-screen").fadeIn('slow');
                    e.preventDefault();
                    
                });
                $("h1").mouseover(function(){$('#about').show();});
                $("h1").mouseout(function(){$('#about').hide();});
                
                $('#currentFilter>li>a').click(function(e){
                    if ($(this).attr("id") == null){
                      setFilter($(this).text());
                      setFilterHTML($(this).text());

                    }
                    else{
                      setFilter($(this).attr("id"));
                      setFilterHTML($(this).text());
                    }
                    showLoading();
                    redrawMap();
                    e.preventDefault();
                });
                $('#currentView>li>a').click(function(e){
                    
                    setView($(this).attr("id"));
                    setViewHTML($(this).attr("id"));
                    
                    showLoading();
                    redrawMap();
                    e.preventDefault();
                });
                
                $('#zoom-GB').click(function(e){window.map.setZoom(11); window.map.setCenter(window.mapCenter); setZoomHTML($(this).text()); e.preventDefault();} );
                $('#zoom-MA').click(function(e){window.map.setZoom(9); window.map.setCenter(window.mapCenter); setZoomHTML($(this).text()); e.preventDefault();});
                $('#zoom-USA').click(function(e){window.map.setZoom(5); window.map.setCenter(new google.maps.LatLng(39.8282, -98.5795)); setZoomHTML($(this).text()); e.preventDefault();});
                $('#zoom-world').click(function(e){window.map.setZoom(3); setZoomHTML($(this).text()); e.preventDefault();});
                

                window.markers = [];
                var stylesArray = [
                                      {
                                        "featureType": "road",
                                        "stylers": [
                                          { "visibility": "off" }
                                        ]
                                      },{
                                        "featureType": "poi",
                                        "stylers": [
                                          { "visibility": "off" }
                                        ]
                                      },{
                                        "featureType": "water",
                                        "stylers": [
                                          { "visibility": "simplified" }
                                        ]
                                      },{
                                        "featureType": "landscape",
                                        "stylers": [
                                          { "visibility": "on" },
                                          { "color": "#fdfdfd" }
                                        ]
                                      },{
                                        "featureType": "transit",
                                        "stylers": [
                                          { "visibility": "off" }
                                        ]
                                      },{
                                      },{
                                        "featureType": "landscape",
                                        "stylers": [
                                          { "visibility": "on" },
                                          { "color": "#faf9fb"}
                                          //"color": "#666666" }
                                        ]
                                      },{
                                        "featureType": "water",
                                        "stylers": [
                                          { "visibility": "simplified" },
                                          { "color": "#9cf0f4" }
                                        ]
                                      },
                                    ];
               
                
                drawMap();
                loadPlaceMetadata();
                setFilter("all-stories");
                setView("distribution");
                loadTownPolygons();
                loadNeighborhoodPolygons();
                redrawMap();
                
                var image = 'ui/images/news_icon_transparent.png';
                var image_sports = 'ui/images/icon_sports.png';
                var image_arts = 'ui/images/icon_arts.png';
                var image_business = 'ui/images/icon_business.png';
                var image_editorial = 'ui/images/icon_oped.png';
                var image_metro = 'ui/images/icon_metro.png';
                var image_livingarts = 'ui/images/icon_livingarts.png';
                var image_books = 'ui/images/icon_books.png';
                var image_movies = 'ui/images/icon_movies.png';
                var image_obits = 'ui/images/icon_obits.png';
                var image_food = 'ui/images/icon_food.png';
                var image_letters = 'ui/images/icon_letters.png';
                var image_schools = 'ui/images/icon_schools.png';
                var image_travel = 'ui/images/icon_travel.png';
                var image_ideas = 'ui/images/icon_ideas.png';
                var image_realestate = 'ui/images/icon_realestate.png';

                function setZoomHTML(text){
                  $('#zoom-button').html("<strong>Zoom:</strong> " + text + ' <span class="caret"></span>' );
                }
                function setFilterHTML(text){
                  $('#filter-button').html("<strong>Map:</strong> " + text + ' <span class="caret"></span>' );
                }
                function setViewHTML(text){
                  if (text =="distribution")
                      text = "Distribution";
                  else
                      text = "Per Capita"
                  $('#view-button').html("<strong>View:</strong> " + text + ' <span class="caret"></span>' );
                }
                function showLoading(){
                  $('.results').html('<h4 style="text-align: center"><img src="ui/images/loading.gif" style="padding-right:5px">Loading...</h4>');
                }
                function switchFromPerCapitaToDistribution(){
                  hidePolygons();
                  $('#per-capita-key').fadeOut();
                  $('#headlines').removeClass("scrolling");
                  $('#headlines').empty();
                  showLoading();
                   $('button').removeClass('active');
                }
                function switchFromDistributionToPerCapita(){
                     $('button').removeClass('active');
                     hideMarkers();
                    
                }
                 function log10(num){
                    return Math.log(num) / Math.LN10;
                 }
                function loadPlaceMetadata(){
                  window.metadata = {};
                  var result = $.csv.toObjects(getCSV());

                  for (var i=0;i<result.length;i++){
                    row = result[i];
                    window.metadata[row.cityorneighborhood] = row;
                  }
                 

                }
                function drawMap(){
                    var mapOptions = {
                      center: window.mapCenter,
                      zoom: 11,
                      mapTypeId: google.maps.MapTypeId.ROADMAP,
                      styles:stylesArray,
                      disableDefaultUI: true,
                      zoomControl: true,
                      zoomControlOptions: {
                        style: google.maps.ZoomControlStyle.LARGE,
                        position: google.maps.ControlPosition.RIGHT_TOP
                      }
                     
                    };
                    var articlesWithGeoData = 0;

                    window.map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
                    
       
                }
                
                function showMarkers() {
                    for (var i = 0; i < window.markers.length; i++ ) {
                      window.markers[i].setVisible(true);
                    }
                     window.markerCluster = new MarkerClusterer(window.map, window.markers,{gridSize: 50,maxZoom:11});
                }
                function hideMarkers() {
                    for (var i = 0; i < window.markers.length; i++ ) {
                      window.markers[i].setVisible(false);
                    }
                    if (window.markerCluster)
                      window.markerCluster.clearMarkers();
  
                    window.markerCluster = null;
                }
                function clearMarkers() {
                  for (var i = 0; i < window.markers.length; i++ ) {
                    window.markers[i].setMap(null);
                  }
                  if (window.markerCluster)
                    window.markerCluster.clearMarkers();
                  window.markers = null;
                  window.markerCluster = null;
                }

                function addMarker(article,metaDataString) {
                    var articleURL = "";
                    var point = new google.maps.LatLng(article.latitude[0], article.longitude[0]);

                    var icon = image;
                    switch(article.printsection[0]){
                      case "Sports":
                        icon = image_sports;
                        break;
                      case "Metro":
                        icon = image_metro;
                        break;
                      case "Arts":
                        icon = image_arts;
                        break;
                      case "LivingArts":
                        icon = image_livingarts;
                        break;
                      case "Business":
                        icon = image_business;
                        break;
                      case "Editorial":
                        icon = image_editorial;
                        break;
                      case "EditorialOpinion":
                        icon = image_editorial;
                        break;
                      case "Obits":
                        icon = image_obits;
                        break;
                      case "Books":
                        icon = image_books;
                        break;
                      case "Movies":
                        icon = image_movies;
                        break;
                      case "Food":
                        icon = image_food;
                        break;
                      case "Travel":
                        icon = image_travel;
                        break;
                      case "Schools":
                        icon = image_schools;
                        break;
                      case "College":
                        icon = image_schools;
                        break;
                      case "Letters":
                        icon = image_letters;
                        break;
                      case "RealEstate":
                        icon = image_realestate;
                        break;
                      case "Ideas":
                        icon = image_ideas;
                        break;

                        
                    }
                    var marker = new google.maps.Marker({
                        position:point,
                        map: window.map,
                        title: "Boston Globe story",
                        icon:icon
                    });
                    window.markers.push(marker);
                    google.maps.event.addListener(marker, 'mouseover', function() {
                          
                          var url = window.couchURL + 'boston-globe-articles/_design/globe/_view/article_summary?key="'+ article.id + '"';
                          console.log(url);
                          var jqxhr =  $.getJSON(url, function() {
                  
                          })
                           .success(function(json) {

                               if (json.rows.length > 0) {

                                    var articleSummary = json.rows[0].value;
                                    marker.title = articleSummary.headline[0];
                                    articleURL = articleSummary.canonicalurl[0];
                                    var contentString = '<div id="content">';
                                     if (articleSummary.headline[0]){
                                          contentString+='<h3 id="firstHeading" class="firstHeading">'+
                                              articleSummary.headline[0] 
                                          +'</h3>';
                                      }
                                     
                                    contentString += '<div id="bodyContent">'+'<p>'+ metaDataString + articleSummary.summary[0] +'</p></div></div>';
                                          
                                    window.currentMarkerInfoWindow = new google.maps.InfoWindow({
                                        content: $(contentString).html()
                                    });
                                    window.currentMarkerInfoWindow.open(window.map,marker);
                                    
                                    google.maps.event.addListener(marker, 'click', function() {
                                        if (articleURL)
                                          window.open(articleURL,"_blank")
                                        return false;
                                    });
                                }
                                
                                
                            })
                        .error(function(data) { console.log(data) })
                        .complete(function() { 
                          
                        }); 
 
                    });
                    
                    google.maps.event.addListener(marker, 'mouseout', function() {
                      window.currentMarkerInfoWindow.close();
                    });
                    
                }

                //setFilter clears out markers on map and hides polygons because data has changed
                function setFilter(filter){
                    window.currentFilter = filter;
                    if (window.markers != null && window.markers.length > 0)
                        clearMarkers();
                    window.markers = [];
                    hidePolygons();

                    
                }

                //setView handles UI changes between percap & distribution views of the data
                function setView(view){
                    if (window.currentView !== null && window.currentView != view){
                        if (window.currentView == "distribution")
                            switchFromDistributionToPerCapita();
                        else
                            switchFromPerCapitaToDistribution();
                    }
                    window.currentView = view;
                }
                function redrawMap(){
                  if (window.currentView == "distribution"){
                      switch(window.currentFilter)
                      {
                        case "all-stories":
                          couchView = "all_articles";
                          break;
                        case "all-stories-world":
                          couchView = "all_articles_world";
                          break;
                        case "page1-stories":
                          couchView = "all_articles_page_1";
                          break;
                        case "yesterday-stories":
                          var d = new Date();
                          d.setDate(d.getDate() - 1);
                          couchView = 'all_articles_by_date?key="' + d.getFullYear() + ((d.getMonth() + 1 < 10) ? "0" : "") + (d.getMonth() + 1)  + ((d.getDate() + 1 < 10) ? "0" : "") + d.getDate() + '"';
                          break;
                        default:
                          couchView = 'all_articles_by_printsection?key="'+window.currentFilter +'"';
                      }
                      showArticleDistribution(couchView);
                  }
                  else if (window.currentView == "per-capita"){
                      switch(window.currentFilter)
                      {
                        case "all-stories":
                          couchView = "city_count?";
                          break;
                        case "all-stories-world":
                          couchView = "city_count?";
                          break;
                        case "page1-stories":
                          couchView = "city_count_page_1?";
                          break;
                        case "yesterday-stories":
                          var d2 = new Date();
                          d2.setDate(d2.getDate() - 1);
                          var yesterday = d2.getFullYear() + ((d2.getMonth() + 1 < 10) ? "0" : "") + (d2.getMonth() + 1)  + ((d2.getDate() + 1 < 10) ? "0" : "") + d2.getDate();
                          couchView = 'city_count_yesterday?startkey=["'+yesterday+'","A","A"]&endkey=["'+yesterday+'","Z","Z"]';
                          break;
                        default:
                          couchView = 'city_count_printsection?startkey=["'+window.currentFilter+'","A","A"]&endkey=["'+window.currentFilter+'","Z","Z"]';
                          
                      }
                      showArticlesPerCapita(couchView);

                  }
                }
                function showMetadata(){
                  var url = window.couchURL + 'boston-globe-articles/_design/globe/_view/metadata';
                  console.log(url);
                  var jqxhr =  $.getJSON(url, function() {
                
                    })
                     .success(function(json) {
                       
                        window.currentResultCount = json.rows.length;
                        //TODO - double check this is getting most recent count of articles once DB not re-created every night
                         if (json.rows.length > 0) {
                              for (i=0; i<json.rows.length; i++) {
                                  var metadataDate = json.rows[i].key;
                                  var metadata = json.rows[i].value;
                                  $('#total_articles_available').text( metadata.total_articles_added + metadata.filtered_articles_no_geodata + metadata.filtered_articles_bad_geodata);
                                  $('#total_articles_added').text(addCommas(metadata.total_articles_added));
                                  $('#filtered_articles_no_geodata').text(addCommas(metadata.filtered_articles_no_geodata));
                                  $('#filtered_articles_bad_geodata').text(addCommas(metadata.filtered_articles_bad_geodata));      
                              }
                              
                              
                          }
                          else{
                              console.log("Couldn't retrieve DB metadata - something's up, man.")
                          }
                          
                      })
                  .error(function(data) { console.log(data) })
                  .complete(function() { 
                    console.log("Loaded metadata")
                  }); 
                  
                }
                function showArticleDistribution(couchView){
                  var url = window.couchURL + 'boston-globe-articles/_design/globe/_view/' + couchView;
                  console.log(url);
                  var jqxhr =  $.getJSON(url, function() {
                
                    })
                     .success(function(json) {
                       
                        window.currentResultCount = json.rows.length;
                         if (json.rows.length > 0) {
                              for (i=0; i<json.rows.length; i++) {
                                  var article = json.rows[i].value;
                                    
                                      var metaDataString = "<b>";
                                      if (article.printpublicationdate[0])
                                          
                                          metaDataString+=  article.printpublicationdate[0].substring(4,6) +"/"+ article.printpublicationdate[0].substring(6,8) + "/"+ article.printpublicationdate[0].substring(0,4) +". ";

                                      if (article.printsection[0]){
                                         metaDataString+=article.printsection[0] +' Section. ';
                                      }
                                      if (article.printpagenumber[0]){
                                        metaDataString+= 'Page '+article.printpagenumber[0] +'. ';
                                      }
                                      metaDataString +="</b>";
                                      
                                      article.id = json.rows[i].id;
                                      
                                      addMarker(article,metaDataString); 
                                      
                                  
                              }
                              
                              
                          }
                          else{
                              //$('.results').html('<h4>No stories found</h4>');
                          }
                          showResultsCount();
                      })
                  .error(function(data) { 
                    $('.results').html('<h4 style="text-align: center">Sorry! Error loading data.</h4>');
                    console.log("Error: " + data) 
                  })
                  .complete(function() { 
                    showMarkers();
                  }); 
                  
                }
                function showArticlesPerCapita(couchView){
                    var url = window.couchURL + 'boston-globe-articles/_design/globe/_view/'+couchView+'&group=true';
                    console.log(url)
                    var jqxhr =  $.getJSON(url, function() {
                  
                      })
                       .success(function(json) { 
                          
                          window.currentResultCount = 0
                           if (json.rows.length > 0) 
                           {
                                var maxValue = 0;
                                var minValue = 0;
                                
                                for (i=0; i<json.rows.length; i++) {
                                    var town = json.rows[i].key[0];
                                    var neighborhood = json.rows[i].key[1];
                                    //ok, this is a pain, if we are filtering by print section i.e. "Sports"
                                    // then key returned is 3 part - section, town, neighborhood
                                    if (json.rows[i].key.length == 3){
                                      town = json.rows[i].key[1];
                                      neighborhood = json.rows[i].key[2];
                                    }

                                    window.currentResultCount +=json.rows[i].value;
                                    var isNeighborhood = false;
                                    
                                    if (town != null && town.length > 0 )
                                    {
                                      
                                      //Store # articles for later display
                                      if (town != "Boston" && window.townPolygons[town.toUpperCase()] != null)  
                                      {  window.townPolygons[town.toUpperCase()].articleCount =json.rows[i].value;
                                        
                                      }
                                      else if (town == "Boston" && neighborhood.length > 0){
                                          
                                            window.neighborhoodPolygons[neighborhood].articleCount =json.rows[i].value;
                                            isNeighborhood = true;
                                        
                                      }
                                      else{
                                        continue;
                                      }

                                      var articleCount = json.rows[i].value;
                                      var metadata = isNeighborhood? window.metadata[neighborhood] : window.metadata[town];
                                      
                                      //Filtering out crazy neighborhoods that throw off max & mins
                                      if(metadata != null && neighborhood != "Leather District" && neighborhood != "South Boston Waterfront" && neighborhood != "Bay Village" && town != "Berlin" && town != "Georgetown" && town != "Rochester"){
                                        var population = metadata.year2010;
                                        var perCapita = articleCount/population;

                                        if (maxValue == 0 && minValue == 0){
                                          maxValue =perCapita;
                                          minValue =perCapita;
                                        }
                                        if (perCapita>maxValue){
                                          maxValue =perCapita;
                                         
                                        } else if(perCapita<minValue){
                                          minValue=perCapita;
                                        }
                                      }
                                    }
                                }
                                var diff = maxValue - minValue;
                                var step = diff/8;
                                

                                for (i=0; i<json.rows.length; i++) {
                                    var town = json.rows[i].key[0];
                                    var neighborhood = json.rows[i].key[1];
                                    
                                    //ok, this is a pain, if we are filtering by print section i.e. "Sports"
                                    // then key returned is 3 part - section, town, neighborhood
                                    if (json.rows[i].key.length == 3){
                                      town = json.rows[i].key[1];
                                      neighborhood = json.rows[i].key[2];
                                    }

                                    var isNeighborhood = (town == "Boston" && neighborhood.length > 0);

                                    if ((town != null && town.length > 0 && town != "Berlin" && town != "Georgetown" && town != "Rochester") || (isNeighborhood))
                                    {

                                      var articleCount = json.rows[i].value;
                                      var metadata = isNeighborhood? window.metadata[neighborhood] : window.metadata[town];
                                      
                                     
                                      if (metadata !=null){
                                        var population = metadata.year2010;
                                        var perCapita = articleCount/population;
                                        
                                        var geoPolygon = isNeighborhood ? window.neighborhoodPolygons[neighborhood] : window.townPolygons[town.toUpperCase()];
                                        //handle case where multipolys
                                        if (geoPolygon instanceof Array){
                                            
                                            for (var j=0;j<geoPolygon.length;j++){
                                              var poly = geoPolygon[j];
                                              if (poly != null) {
                                                setPolygonOpacity(perCapita,minValue,maxValue,step,poly);
                                              }
                                            }
                                        }
                                        else if (geoPolygon != null) {
                                          setPolygonOpacity(perCapita,minValue,maxValue,step,geoPolygon);
                                        }
                                      }
                                      
                                    }  
                                    //Bad Globe data for these towns from pre-May 2012 Sports bad data
                                    if (town == "Berlin" || town == "Georgetown" || town == "Rochester"){
                                        var geoPolygon = isNeighborhood ? window.neighborhoodPolygons[neighborhood] : window.townPolygons[town.toUpperCase()];
                                        setPolygonGrey(geoPolygon);

                                    } 
                                    
                                }
                                updateMapKey(maxValue,minValue,step);
                            }
                           
                        })
                    .error(function(data) { 
                      console.log(data) ;
                      $('.results').html('<h4 style="text-align: center">Sorry! Error loading data.</h4>');
                    })
                    .complete(function() { 
                      showResultsCount();
                      console.log("Loaded shapes") 
                    }); 
                    

                }
                function showResultsCount(){
                  var resultsText = "aa";
                  if (window.currentFilter == "all-stories")
                    resultsText = " stories in MA retrieved from November 2011 to the present.";
                  else if(window.currentFilter == "all-stories-world")
                    resultsText = " total stories retrieved from November 2011 to the present.";
                  else if(window.currentFilter == "page1-stories")
                    resultsText = " front of section stories retrieved from November 2011 to the present.";
                  else if(window.currentFilter == "yesterday-stories")
                    resultsText = " stories from yesterday.";
                  else
                    resultsText = " " + addCommas(window.currentFilter) + " stories retrieved from November 2011 to the present.";

                  $('.results').html('<h4>'+addCommas(window.currentResultCount) + resultsText + "</h4>");
                }
                function setPolygonGrey(townPolygon){
                  townPolygon.setOptions({fillOpacity: 0.7,strokeWeight:1,strokeOpacity:0.8, strokeColor: "#a65c1c", fillColor:'#CCCCCC'});
                }
                function setPolygonOpacity(articleCount,minValue,maxValue,step,townPolygon){
                  var opacity = 0;
                  if (articleCount >= minValue && articleCount <= minValue + step){
                    opacity=0.2;
                    fillColor = "#ffba2b";
                  }
                  else if (articleCount > minValue + step && articleCount <= minValue + step * 2){
                    opacity=0.5;
                    fillColor = "#ffba2b";
                  }
                  else if (articleCount > minValue + step * 2 && articleCount <= minValue + step * 3){
                    opacity=0.8;
                    fillColor = "#ffba2b";
                  }
                  else if (articleCount > minValue + step * 3 && articleCount <= minValue + step * 4){
                    opacity=1.0;
                    fillColor = "#ffba2b";
                  }
                  else if (articleCount > minValue + step * 4 && articleCount <= minValue + step * 5){
                    opacity=0.8;
                    fillColor = "#a63d03";
                  }
                  else if (articleCount > minValue + step * 5 && articleCount <= minValue + step * 6){
                    opacity=1.0;
                    fillColor = "#a63d03";
                  }
                  else if (articleCount > minValue + step * 6 && articleCount <= minValue + step * 7){
                    opacity=0.8;
                    fillColor = "#FF502B";
                  }
                  else {
                    opacity = 1.0;
                    fillColor = "#FF502B";
                  }
                 
                 
                  townPolygon.setOptions({fillOpacity: opacity,strokeWeight:1,strokeOpacity:0.8, strokeColor: "#a65c1c", fillColor:fillColor});
                 
                }
                function hidePolygons(){
                    for (var town in window.townPolygons) {
                      var geoPolygon = window.townPolygons[town];
                      if (geoPolygon instanceof Array){
                                            
                          for (var j=0;j<geoPolygon.length;j++){
                            var poly = geoPolygon[j];
                            if (poly != null) {
                              poly.setOptions({fillOpacity: 0,strokeWeight:1,strokeOpacity:0.8,strokeColor: "#CCCCCC"});
                            }
                          }
                      }
                      else{
                        geoPolygon.setOptions({fillOpacity: 0,strokeWeight:1,strokeOpacity:0.8,strokeColor: "#CCCCCC"});
                      }
                    }
                    for (var neighborhood in window.neighborhoodPolygons) {
                      var geoPolygon = window.neighborhoodPolygons[neighborhood];
                      if (geoPolygon instanceof Array){
                                            
                          for (var j=0;j<geoPolygon.length;j++){
                            var poly = geoPolygon[j];
                            if (poly != null) {
                              poly.setOptions({fillOpacity: 0,strokeWeight:1,strokeOpacity:0.8,strokeColor: "#CCCCCC"});
                            }
                          }
                      }
                      else{
                        geoPolygon.setOptions({fillOpacity: 0,strokeWeight:1,strokeOpacity:0.8,strokeColor: "#CCCCCC"});
                      }
                    }
                }
                function loadPolygon(townCoordinates,townName,isNeighborhood){

                  var townBoundaryArray = [];
                  for (var j=0; j<townCoordinates.length;j++){
                    var longitude = townCoordinates[j][0];
                    var latitude = townCoordinates[j][1];
                    var latlong = new google.maps.LatLng(latitude, longitude);
                    townBoundaryArray[j] = latlong;
                    
                  }
                  

                  var townPolygon = new google.maps.Polygon({
                    paths: townBoundaryArray,
                    strokeColor: "#CCCCCC",
                    //strokeColor: "#a65c1c",
                    strokeOpacity: 0.8,
                    strokeWeight: 1,
                    fillColor: '#ffba2b',
                    //fillColor: '#FFFFFF',
                    fillOpacity: 0 
                  });
                  
                  townPolygon.setMap(window.map);
                  townPolygon.set("townName",townName);
                 
                  var polywindow = new google.maps.InfoWindow();

                  google.maps.event.addListener(townPolygon, 'click', function(event) {
                        
                        if (window.currentInfoWindow){
                          window.currentInfoWindow.close();
                        }
                        window.currentInfoWindow = polywindow;

                        $('#headlines').empty();
                        
                        var name = this.get('townName');
                        
                        name = name.toProperCase();
                        var metadata = window.metadata[name];

                        var population = metadata.year2010;
                        var articleCount = isNeighborhood ? window.neighborhoodPolygons[name].articleCount : window.townPolygons[name.toUpperCase()].articleCount;
                        if (articleCount === null)
                            articleCount = 0;
                        var perCapita = articleCount / population;


                        
                        $('#headlines').append("<h4>"+name + " Headlines" + ((window.currentView == "page1") ? "<br/>Page 1" : "") + ((window.currentView == "yesterday") ? "<br/>Yesterday" : "" )+ "</h4>");
                        polywindow.setPosition(event.latLng);


                        //Load words into popup window
                        var jqxhr =  $.getJSON(window.couchURL + 'boston-globe-articles/_design/nltk/_view/place_frequency?limit=1&startkey=["'+ name +'"]&endkey=["'+name+'",{}]', function() {
                            console.log(window.couchURL + 'boston-globe-articles/_design/nltk/_view/place_frequency?limit=1&startkey=["'+ name +'"]&endkey=["'+name+'",{}]')
                        })
                       .success(function(json) {
                              if (json.rows.length ==0){
                                placeWords = "<div>No place words available for this town or neighborhood."
                              } else {
                                var words = json.rows[0].value.freqdist;
                                var lineHeight = words[1][1] + 1;
                                placeWords = '<div style="line-height:'+ lineHeight +'em">';
                                for (i=0; i<words.length; i++) {

                                  var word = words[i][0];
                                  if (word == "said" || word =="cq")
                                      continue;
                                  if (word.toLowerCase() != name.toLowerCase()){
                                    
                                    var fontSize = words[i][1] + 1;
                                    
                                    placeWords += " <span class='label' style='margin-right:5px;margin-bottom:5px;font-size:"+Math.max(fontSize,0.75)+"em'>"+ word+"</span>";
                                  }
                                  
                               }
                             }
                             placeWords += "</div>";
                             polywindow.setContent('<h3 id="firstHeading" class="firstHeading">'+name+ "</h3>" + "<br/>"+
                                                                  
                                                                  //addCommas(articleCount) + " stories" + "<br/>"+
                                                                  //addCommas(population) + " Residents"+"<br/>"+
                                                                  //"Stories per capita for this time period: " + perCapita.toFixed(5) +
                                                                  //"<h4>Words associated with "+name+":</h4>"+
                                                                  placeWords);
                        

                              polywindow.open(window.map);
                             
                          })
                      .error(function(data) { console.log(data) })
                      .complete(function() { console.log("Loaded place frequencies") }); 

                        var view = "headline_by_city";
                        if (isNeighborhood)
                            view = "headline_by_neighborhood";
                        
                        if (window.currentView =="page1")
                            view += "_page_1";
                        else if (window.currentView == "yesterday")
                            view += "_yesterday"
                        var jqxhr =  $.getJSON(window.couchURL + 'boston-globe-articles/_design/globe/_view/'+view+'?key="'+name+'"', function() {

                
                          })
                         .success(function(json) {  
                                var printed = 0;
                               for (i=0; i<json.rows.length; i++) {
                                  var headline = json.rows[i].value;

                                  if (headline.headline != null)
                                  {
                                    printed++;
                                    var text = headline.headline;
                                    if (headline.canonicalurl)
                                      text = '<a target="_blank" href="'+headline.canonicalurl+'">' + text + '</a>';
                                    if (i%2==0)
                                    {
                                      
                                      if (headline.printpagenumber == "1")
                                        $('#headlines').append("<p class='stripe page1'>" + text+"</p>");
                                      else
                                        $('#headlines').append("<p class='stripe'>" + text +"</p>");
                                    }
                                    else{
                                        if (headline.printpagenumber == "1")
                                          $('#headlines').append("<p class='page1'>" + text +"</p>"); 
                                        else 
                                          $('#headlines').append("<p>" + text +"</p>");
                                    }
                                  }
                               }
                               if (json.rows.length ==0 || printed ==0)
                                  $('#headlines').append("<p>No headlines available. Not all stories have a headline.</p>");
                               $('#headlines').addClass("scrolling");
                            })
                        .error(function(data) { console.log(data) })
                        .complete(function() { console.log("Loaded city & neighborhood headlines");return false; }); 
                      return false;
                          
                  });
                  return townPolygon;

                }
                
                function loadTownPolygons(){
                  
                  var jqxhr =  $.getJSON('data/shapefiles/townsShapeFiles/MATowns.json', function() {
                      
                    })
                    .success(function(data) {   
                      window.townPolygons = {};
                      var polywindow = new google.maps.InfoWindow();
                      for (var i = 0; i < data.features.length; i++) {
                        var town = data.features[i];
                        var townName = town.properties.TOWN;
                        
                        var townPolygon = null;
                        if (townName != "Boston" && townName != "boston"){
                           //Handle multipolygons - what a pain!
                          if (town.geometry.type == "MultiPolygon"){
                             
                              var townPolygonArray = [];
                             
                             for (var j=0;j<town.geometry.coordinates.length;j++){
                                townPolygon = loadPolygon(town.geometry.coordinates[j][0], townName,false);
                                townPolygonArray[j] =townPolygon;
                             }
                              window.townPolygons[townName]=townPolygonArray;
                          } else {
                              townPolygon =loadPolygon(town.geometry.coordinates[0], townName,false);
                              window.townPolygons[townName]=townPolygon;
                          }
                        }
                      }
                    })
                    .error(function(data) { console.log(data) })
                    .complete(function() { console.log("Loaded MA Towns from GEOJSON...") });
                }
                function loadNeighborhoodPolygons(){
                  
                  var jqxhr =  $.getJSON('data/shapefiles/neighborhoodsShapeFiles/neighborhoods.json', function() {
                      
                    })
                    .success(function(data) {   
                      window.neighborhoodPolygons = {};
                      var polywindow = new google.maps.InfoWindow();
                      for (var i = 0; i < data.features.length; i++) {
                        var neighborhood = data.features[i];
                        var neighborhoodName = neighborhood.properties.name;
                        
                        var neighborhoodPolygon = null;
                         //Handle multipolygons - what a pain!
                        if (neighborhood.geometry.type == "MultiPolygon"){
                           
                            var neighborhoodPolygonArray = [];
                           
                           for (var j=0;j<neighborhood.geometry.coordinates.length;j++){
                              neighborhoodPolygon = loadPolygon(neighborhood.geometry.coordinates[j][0], neighborhoodName,true);
                              neighborhoodPolygonArray[j] =neighborhoodPolygon;
                           }
                            window.neighborhoodPolygons[neighborhoodName]=neighborhoodPolygonArray;
                        } else {
                            neighborhoodPolygon =loadPolygon(neighborhood.geometry.coordinates[0], neighborhoodName,true);
                            window.neighborhoodPolygons[neighborhoodName]=neighborhoodPolygon;
                        }
                      }
                    })
                    .error(function(data) { console.log(data) })
                    .complete(function() { console.log("Loaded Boston Neighborhoods from GEOJSON...") });
                }
                function updateMapKey(maxValue,minValue,step){
                  for (var i=1; i<10;i++){
                    if (i == 9)
                        $('#key9').text( " > " + highVal);
                    else{
                      var lowVal = (minValue + (step * (i - 1))).toFixed(6);
                      var highVal = (minValue + (step * i)).toFixed(6);
                      $('#key' + i).text( lowVal + " - " + highVal );
                    }

                  }
                  $('#per-capita-key').fadeIn();

                }
            }); //end document ready ?
       
        String.prototype.toProperCase = function () {
            return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        };
        function addCommas(nStr)
        {
          nStr += '';
          x = nStr.split('.');
          x1 = x[0];
          x2 = x.length > 1 ? '.' + x[1] : '';
          var rgx = /(\d+)(\d{3})/;
          while (rgx.test(x1)) {
            x1 = x1.replace(rgx, '$1' + ',' + '$2');
          }
          return x1 + x2;
        };
        function getCSV(){
          return "cityorneighborhood,year2000,year2010,percentchange,medianhouseholdincome,percentbelowpoverty,percentunemployed,percentnonwhite\r\nAbington,14605,15985,9.45,74589,4.4,6.2,4.6\r\nActon,20331,21924,7.84,105523,3.8,4.2,23.1\r\nAcushnet,10161,10303,1.4,62457,4.6,10.1,3.6\r\nAdams,8809,8485,-3.68,38340,10.3,11.4,4.2\r\nAgawam,28144,28438,1.04,62664,8.1,5.3,5.4\r\nAlford,399,494,23.81,82500,3.7,1.6,1.9\r\nAmesbury,16450,16283,-1.02,74968,3.7,7.2,3.5\r\nAmherst,34874,37819,8.44,50063,28.5,11.6,21\r\nAndover,31247,33201,6.25,111002,3.7,5.7,13.2\r\nAquinnah,344,311,-9.59,57500,10.1,10.7,66.8\r\nArlington,42389,42844,1.07,82771,4.9,5.1,14\r\nAshburnham,5546,6081,9.65,80000,5.4,6.9,6.9\r\nAshby,2845,3074,8.05,80143,4.2,4.8,2.2\r\nAshfield,1800,1737,-3.5,63438,9.2,5.2,2.7\r\nAshland,14674,16593,13.08,92974,3.1,5.5,13.1\r\nAthol,11299,11584,2.52,47099,9.1,10.2,6.6\r\nAttleboro,42068,43593,3.63,64634,7.2,8.1,11.3\r\nAuburn,15901,16188,1.8,71375,5.8,6.3,3.2\r\nAvon,4443,4356,-1.96,67313,3.1,11,13.7\r\nAyer,7287,7427,1.92,55863,17.2,10.8,15.4\r\nBarnstable,47821,45193,-5.48,62264,7.1,6.3,9.1\r\nBarre,5113,5398,5.57,75423,7.5,11.4,1\r\nBecket,1755,1779,1.37,42031,13.7,6.2,3.6\r\nBedford,12595,13320,5.76,107639,4.6,5.7,13.8\r\nBelchertown,12968,14649,12.96,77090,5.7,4.8,7.1\r\nBellingham,15314,16332,6.65,78290,4.9,5.9,5\r\nBelmont,24194,24729,2.21,95197,4.9,3.7,15.3\r\nBerkley,5749,6411,11.52,81125,6.2,5.5,2.7\r\nBerlin,2380,2866,20.42,92917,1.8,5.6,4.2\r\nBernardston,2155,2129,-1.21,52875,4.1,5,0.9\r\nBeverly,39862,39502,-0.9,66671,9,5.4,6.8\r\nBillerica,38981,40243,3.24,87073,3.3,5.9,9.7\r\nBlackstone,8804,9026,2.52,71875,3.8,5,5.3\r\nBlandford,1214,1233,1.57,72188,5.5,6.4,1.7\r\nBolton,4148,4897,18.06,125741,2.3,6.5,3.2\r\nBoston,589141,617594,4.83,50684,21.2,9.3,46.1\r\nBourne,18721,19754,5.52,61418,8.2,6.1,4.2\r\nBoxborough,4868,4996,2.63,102222,6.4,6.2,16.6\r\nBoxford,7921,7965,0.56,143045,2.1,6.1,3.5\r\nBoylston,4008,4355,8.66,88214,1.1,2.6,4.1\r\nBraintree,33828,35744,5.66,81146,5.2,7,10.7\r\nBrewster,10094,9820,-2.71,58374,9.8,5,3.4\r\nBridgewater,25185,26563,5.47,86002,6,6.7,7.7\r\nBrimfield,3339,3609,8.09,75625,3.5,9.5,0.4\r\nBrockton,94304,93810,-0.52,49913,14.6,12.7,49.1\r\nBrookfield,3051,3390,11.11,60189,2.1,4.8,1.2\r\nBrookline,57107,58732,2.85,95448,13.1,3.9,22.8\r\nBuckland,1991,1902,-4.47,49485,10.3,6.9,1.5\r\nBurlington,22876,24498,7.09,90341,2.8,7,18.3\r\nCambridge,101355,105162,3.76,64865,15,5.8,31.8\r\nCanton,20775,21561,3.78,89705,4.3,5.9,13.4\r\nCarlisle,4717,4852,2.86,155000,6,8,11.7\r\nCarver,11163,11509,3.1,71112,5.6,10.3,4.9\r\nCharlemont,1358,1266,-6.77,59063,10.2,9.9,4.8\r\nCharlton,11263,12981,15.25,87758,3.5,5.4,2.6\r\nChatham,6625,6125,-7.55,65990,7,6.5,7.7\r\nChelmsford,33858,33802,-0.17,92550,3.9,6.2,9.9\r\nChelsea,35080,35177,0.28,40487,24.2,11.5,51.8\r\nCheshire,3401,3235,-4.88,57419,12.1,5.9,1\r\nChester,1308,1337,2.22,55208,7.1,5.9,0.5\r\nChesterfield,1201,1222,1.75,58750,4.3,5.6,0.6\r\nChicopee,54653,55298,1.18,44226,15.4,9.2,13.4\r\nChilmark,843,866,2.73,72917,8.1,3.2,3.5\r\nClarksburg,1686,1702,0.95,52054,3.2,2.8,0.4\r\nClinton,13435,13606,1.27,58826,8.5,7.1,10.7\r\nCohasset,7261,7542,3.87,114214,1.2,5.2,1.8\r\nColrain,1813,1671,-7.83,58611,7.9,5,5.6\r\nConcord,16993,17668,3.97,119858,4.3,3.5,10\r\nConway,1809,1897,4.86,78309,6.9,6.6,4.1\r\nCummington,978,872,-10.84,60000,13.5,3.8,0.8\r\nDalton,6892,6756,-1.97,57222,6.6,8.7,2.6\r\nDanvers,25212,26493,5.08,75310,5.7,5.4,2.8\r\nDartmouth,30666,34032,10.98,70007,4.6,6,6.4\r\nDedham,23464,24729,5.39,80865,4.9,6.1,9.6\r\nDeerfield,4750,5125,7.89,61912,7,5.3,2.6\r\nDennis,15973,14207,-11.06,50642,11.9,6.6,7.7\r\nDighton,6175,7086,14.75,83621,3.5,5.3,1.4\r\nDouglas,7045,8471,20.24,86214,2.1,7.7,3.4\r\nDover,5558,5589,0.56,164583,2,2.7,11.7\r\nDracut,28562,29457,3.13,70833,3.6,6.1,7.2\r\nDudley,10036,11390,13.49,64782,7.6,7.6,6.5\r\nDunstable,2829,3179,12.37,113594,4.6,4.7,3.6\r\nDuxbury,14248,15059,5.69,114565,2.6,6.3,1\r\nEast Bridgewater,12974,13794,6.32,78492,6.2,6.3,2\r\nEast Brookfield,2097,2183,4.1,71964,7.1,5.5,2.6\r\nEast Longmeadow,14100,15720,11.49,77956,3,4,6.2\r\nEastham,5453,4956,-9.11,58750,5.8,9.6,2.4\r\nEasthampton,15994,16053,0.37,54657,6.2,6.4,6.3\r\nEaston,22299,23112,3.65,86050,2.8,6.5,6.3\r\nEdgartown,3779,4067,7.62,67625,11.7,2.6,0.9\r\nEgremont,1345,1225,-8.92,51856,4.7,3.3,2.6\r\nErving,1467,1800,22.7,51458,8.5,8.7,4.8\r\nEssex,3267,3504,7.25,76989,0.6,4.1,1.1\r\nEverett,38037,41667,9.54,49737,11.9,9,25.7\r\nFairhaven,16159,15873,-1.77,54144,10.2,6.5,3.3\r\nFall River,91938,88857,-3.35,34236,20.2,13.2,10.7\r\nFalmouth,32660,31531,-3.46,62392,6.5,6,7.5\r\nFitchburg,39102,40318,3.11,47019,19.4,10.4,17.7\r\nFlorida,676,752,11.24,53333,5.1,9.1,6.9\r\nFoxborough,16246,16865,3.81,93397,1.7,4.5,4.6\r\nFramingham,66910,68318,2.1,64061,8.8,5.2,27.1\r\nFranklin,29560,31635,7.02,89330,4.4,5.8,7.2\r\nFreetown,8472,8870,4.7,82308,4.8,5.8,3.8\r\nGardner,20770,20228,-2.61,48333,11.4,9.4,9\r\nGeorgetown,7377,8183,10.93,101875,1.6,5.9,1.2\r\nGill,1363,1500,10.05,58487,5.9,5.8,2.3\r\nGloucester,30273,28789,-4.9,60506,7.8,6.1,3.3\r\nGoshen,921,1054,14.44,70625,0.6,2.6,5.6\r\nGosnold,86,75,-12.79,46250,0,0,2\r\nGrafton,14894,17765,19.28,91743,6.5,6,11.8\r\nGranby,6132,6240,1.76,66726,5.7,6.4,4.8\r\nGranville,1521,1566,2.96,69125,1.3,5.8,3\r\nGreat Barrington,7527,7104,-5.62,52843,8.5,4.5,11\r\nGreenfield,18168,17456,-3.92,45261,14.9,8.4,6.1\r\nGroton,9547,10646,11.51,123853,2.3,4.5,2.9\r\nGroveland,6038,6459,6.97,84232,4,5.4,0.8\r\nHadley,4793,5250,9.53,69911,7.1,3.4,5.8\r\nHalifax,7500,7518,0.24,81855,5.6,7,4.5\r\nHamilton,8315,7764,-6.63,99732,6.5,5.4,13.6\r\nHampden,5171,5139,-0.62,78869,2.6,6.4,2.2\r\nHancock,721,717,-0.55,74205,8.3,3.9,0.7\r\nHanover,13164,13879,5.43,100233,3.4,6.9,3.3\r\nHanson,9495,10209,7.52,81964,4.7,8.1,6.2\r\nHardwick,2622,2990,14.04,57866,9.8,8.4,3.6\r\nHarvard,5981,6520,9.01,141274,5.5,5.1,11.4\r\nHarwich,12386,12243,-1.15,54958,7.9,6.3,4.8\r\nHatfield,3249,3279,0.92,53939,11.2,8.4,2.7\r\nHaverhill,58969,60879,3.24,61956,11.1,8.1,18.4\r\nHawley,336,337,0.3,65313,10.2,9.7,0\r\nHeath,805,706,-12.3,68875,12.8,5.9,0.5\r\nHingham,19882,22157,11.44,98890,3.1,5,2.7\r\nHinsdale,1872,2032,8.55,60766,4.3,5.3,3.5\r\nHolbrook,10785,10791,0.06,62623,3.8,6.3,16.8\r\nHolden,15621,17346,11.04,88405,3.3,6,4.4\r\nHolland,2407,2481,3.07,67596,7.1,7.3,4.6\r\nHolliston,13801,13547,-1.84,103600,1.8,5.2,4.7\r\nHolyoke,39838,39880,0.11,31948,31.7,13.1,15.3\r\nHopedale,5907,5911,0.07,97227,5.9,7.4,3.2\r\nHopkinton,13346,14925,11.83,120240,1.8,4,4.5\r\nHubbardston,3909,4382,12.1,82443,9.5,8.9,3.7\r\nHudson,18113,19063,5.24,74983,7.1,5.9,7.3\r\nHull,11050,10293,-6.85,72166,9.8,5.9,4.9\r\nHuntington,2174,2180,0.28,61912,10.7,5.5,6.4\r\nIpswich,12987,13175,1.45,80816,4.6,7.7,2.1\r\nKingston,11780,12629,7.21,77656,6.4,8.1,4.5\r\nLakeville,9821,10602,7.95,92033,2.4,7.6,6.3\r\nLancaster,7380,8055,9.15,80938,9.2,5.4,13.9\r\nLanesborough,2990,3091,3.38,66458,2.1,3.6,3.7\r\nLawrence,72043,76377,6.02,31631,26.5,8,68.6\r\nLee,5985,5943,-0.7,50599,9.8,10.4,2.4\r\nLeicester,10471,10970,4.77,70362,4.1,8.6,6.4\r\nLenox,5077,5025,-1.02,60604,7.7,3.3,2.7\r\nLeominster,41303,40759,-1.32,55695,9.9,7.3,15.1\r\nLeverett,1663,1851,11.3,69702,17.9,3.4,11.5\r\nLexington,30355,31394,3.42,130637,3.2,4.5,23.2\r\nLeyden,772,711,-7.9,74531,2.6,2,0\r\nLincoln,8056,6362,-21.03,121104,1.7,2.6,13.2\r\nLittleton,8184,8924,9.04,103616,3.5,4,5.1\r\nLongmeadow,15633,15784,0.97,92862,2.4,2.7,6.4\r\nLowell,105167,106519,1.29,50192,17.5,8.5,39.8\r\nLudlow,21209,21103,-0.5,61008,5.5,7.3,6.1\r\nLunenburg,9401,10086,7.29,86568,5.5,6.8,5\r\nLynn,89050,90329,1.44,43200,19.3,9.7,31.9\r\nLynnfield,11542,11596,0.47,87590,4.1,3.1,4.1\r\nMalden,56340,59450,5.52,56347,12.8,9.5,40\r\nManchester,5228,5136,-1.76,105000,3.5,3.7,1.5\r\nMansfield,22414,23184,3.44,94529,5.4,7.1,8.7\r\nMarblehead,20377,19808,-2.79,97097,4.8,4.4,2.9\r\nMarion,5123,4907,-4.22,101006,2.2,4.4,8.9\r\nMarlborough,36255,38499,6.19,71617,8,5.6,14.3\r\nMarshfield,24324,25132,3.32,86486,4.4,5.2,2.9\r\nMashpee,12946,14006,8.19,62645,7.6,3.9,6.3\r\nMattapoisett,6268,6045,-3.56,74877,5,3.9,1.1\r\nMaynard,10433,10106,-3.13,75597,3.6,5.7,4.8\r\nMedfield,12273,12024,-2.03,126048,1.6,4,5.6\r\nMedford,55765,56173,0.73,70102,8.3,6.8,20.4\r\nMedway,12448,12752,2.44,102002,2.8,5.8,5.9\r\nMelrose,27134,26983,-0.56,82482,4.7,5.7,8.9\r\nMendon,5286,5839,10.46,102625,2.2,5,3.7\r\nMerrimac,6138,6338,3.26,75517,3.8,3.8,2.7\r\nMethuen,43789,47255,7.92,61822,7.1,6.2,20.5\r\nMiddleborough,19941,23116,15.92,70757,7.2,7.8,6.5\r\nMiddlefield,542,521,-3.87,66250,0.7,4.1,0\r\nMiddleton,7744,8987,16.05,87728,3.8,7.1,10.4\r\nMilford,26799,27999,4.48,66636,7.7,6.6,10.8\r\nMillbury,12784,13261,3.73,67448,3.4,7.5,5\r\nMillis,7902,7891,-0.14,85472,2.4,9.3,3.4\r\nMillville,2724,3190,17.11,77250,3.2,6.9,1.8\r\nMilton,26062,27003,3.61,97421,3.8,5.6,17.4\r\nMonroe,93,121,30.11,30833,18.2,16.4,0\r\nMonson,8359,8560,2.4,73004,8.4,7.3,3.2\r\nMontague,8489,8437,-0.61,42140,16.8,7.8,9.5\r\nMonterey,934,961,2.89,41625,19.1,16.8,2.6\r\nMontgomery,654,838,28.13,73438,3.3,7.7,1.6\r\nMount Washington,130,167,28.46,65833,3,8.3,2.3\r\nNahant,3632,3410,-6.11,81831,3.1,4,6.4\r\nNantucket,9520,10172,6.85,83347,7.2,2.2,11.4\r\nNatick,32170,33006,2.6,87568,3.5,3.6,12.5\r\nNeedham,28911,28886,-0.09,114365,3.8,3.7,10.2\r\nNew Ashford,247,228,-7.69,69583,5.6,14.1,0.9\r\nNew Bedford,93768,95072,1.39,36172,22.7,10.1,21.7\r\nNew Braintree,927,999,7.77,85417,2.4,6.5,0.5\r\nNew Marlborough,1494,1509,1,57917,3.5,0.5,1.3\r\nNew Salem,929,990,6.57,61471,6.4,7,3.9\r\nNewbury,6717,6666,-0.76,91052,3.7,6,2.4\r\nNewburyport,17189,17416,1.32,76300,5.8,4.9,4.3\r\nNewton,83829,85146,1.57,107696,5.9,4.3,16.6\r\nNorfolk,10460,11227,7.33,113266,3.8,4.2,12.2\r\nNorth Adams,14681,13708,-6.63,35401,16.1,11.3,8.3\r\nNorth Andover,27202,28352,4.23,91741,3.7,5.4,9.6\r\nNorth Attleborough,27143,28712,5.78,77669,4.1,8.5,5.3\r\nNorth Brookfield,4683,4680,-0.06,57196,5.6,5.8,4.1\r\nNorth Reading,13837,14892,7.62,96016,4.6,6.1,3.4\r\nNorthampton,28978,28549,-1.48,52868,13.1,6.1,14.1\r\nNorthborough,14013,14155,1.01,102969,4.4,5.4,11.8\r\nNorthbridge,13182,15707,19.15,68016,5.1,7.3,3.2\r\nNorthfield,2951,3032,2.74,70606,1.8,3.8,1.1\r\nNorton,18036,19031,5.52,77786,4.7,8.8,7.6\r\nNorwell,9765,10506,7.59,108944,1.7,4.1,4.7\r\nNorwood,28587,28602,0.05,72472,6.1,5.4,14.9\r\nOak Bluffs,3713,4527,21.92,59156,9.4,8.8,22.3\r\nOakham,1673,1902,13.69,77396,4.8,7.3,1.7\r\nOrange,7518,7839,4.27,42809,11.8,11.1,3\r\nOrleans,6341,5890,-7.11,56313,5,5.2,1.7\r\nOtis,1365,1612,18.1,63750,11.7,8.6,3.3\r\nOxford,13352,13709,2.67,65845,5.4,9.6,4\r\nPalmer,12497,12140,-2.86,50638,11.8,9.7,3.3\r\nPaxton,4386,4806,9.58,100333,4.3,5.3,7.6\r\nPeabody,48129,51251,6.49,65515,6.1,6.8,8.2\r\nPelham,1403,1321,-5.84,81765,4.7,4.3,4.3\r\nPembroke,16927,17837,5.38,80694,3.4,6.8,2.3\r\nPepperell,11142,11497,3.19,82055,2.7,4.5,2.4\r\nPeru,821,847,3.17,66250,7.9,8.2,2.3\r\nPetersham,1180,1234,4.58,62411,17.5,8.1,5.3\r\nPhillipston,1621,1682,3.76,70493,3.5,7.9,2.8\r\nPittsfield,45793,44737,-2.31,43188,16,8.2,10\r\nPlainfield,589,648,10.02,57054,5.2,8.9,5.4\r\nPlainville,7683,8264,7.56,73645,4.2,4.9,3.9\r\nPlymouth,51701,56468,9.22,74767,6.5,8.6,5.4\r\nPlympton,2637,2820,6.94,87917,2.6,7.8,2\r\nPrinceton,3353,3413,1.79,102853,1.2,3.1,2.7\r\nProvincetown,3431,2942,-14.25,44646,8.8,9,2.7\r\nQuincy,88025,92271,4.82,59803,9.8,8.1,30.6\r\nRandolph,30963,32112,3.71,64607,7.1,8.6,56.2\r\nRaynham,11739,13383,14,75872,2.3,5.3,6\r\nReading,23708,24747,4.38,99130,1.7,5.2,5.1\r\nRehoboth,10172,11608,14.12,87597,4.6,9.8,3\r\nRevere,47283,51755,9.46,49759,14.7,8.2,24.5\r\nRichmond,1604,1475,-8.04,87682,3.2,4.2,1.1\r\nRochester,4581,5232,14.21,95022,3.6,4.6,7.1\r\nRockland,17670,17489,-1.02,64512,5.6,7.9,8.4\r\nRockport,7767,6952,-10.49,70625,3.7,8.3,2\r\nRowe,351,393,11.97,46250,12.2,10,3.9\r\nRowley,5500,5856,6.47,74911,8.3,4.7,0.2\r\nRoyalston,1254,1258,0.32,60385,4.1,10,2.5\r\nRussell,1657,1775,7.12,57750,6.3,6,6.5\r\nRutland,6353,7973,25.5,81295,4.9,8.1,4.4\r\nSalem,40407,41340,2.31,56979,10.8,8.3,17.1\r\nSalisbury,7827,8283,5.83,62917,6.4,8.2,1.7\r\nSandisfield,824,915,11.04,62411,4.5,3.3,6\r\nSandwich,20136,20675,2.68,83325,2.3,5,3.5\r\nSaugus,26078,26628,2.11,71023,5.1,6.2,7.8\r\nSavoy,705,692,-1.84,55500,4.8,2.3,1.3\r\nScituate,17863,18133,1.51,86723,3.1,5.9,3.6\r\nSeekonk,13425,13722,2.21,76283,4.3,6,5.4\r\nSharon,17408,17612,1.17,115172,4.4,5.4,16.6\r\nSheffield,3335,3257,-2.34,47145,8.6,0.6,3.5\r\nShelburne,2058,1893,-8.02,63542,7.8,3.9,4.7\r\nSherborn,4200,4119,-1.93,145250,3,4.1,9.1\r\nShirley,6373,7211,13.15,72598,7.9,5.4,14.7\r\nShrewsbury,31640,35608,12.54,85697,3.7,4.8,20.7\r\nShutesbury,1810,1771,-2.15,67500,8.3,6.2,7.3\r\nSomerset,18234,18165,-0.38,67077,3.2,7.8,4\r\nSomerville,77478,75754,-2.23,61731,14.7,6.3,23.8\r\nSouth Hadley,17196,17514,1.85,62236,6.9,5.4,8.2\r\nSouthampton,5387,5792,7.52,80738,5,3.8,1.1\r\nSouthborough,8781,9767,11.23,140184,1.3,5.9,13.4\r\nSouthbridge,17214,16719,-2.88,47234,12.7,10.3,12.7\r\nSouthwick,8835,9502,7.55,72331,4,4.9,2.1\r\nSpencer,11691,11688,-0.03,63761,6.4,8,6.3\r\nSpringfield,152082,153060,0.64,34628,27.6,14.2,48.6\r\nSterling,7257,7808,7.59,102115,3,5.4,0.8\r\nStockbridge,2276,1947,-14.46,55096,8.7,9.2,6.8\r\nStoneham,22219,21437,-3.52,76574,6.5,6.9,6.3\r\nStoughton,27149,26962,-0.69,67175,7.8,8.6,15.1\r\nStow,5902,6590,11.66,117440,3,5.3,4.5\r\nSturbridge,7837,9268,18.26,71607,9.2,4.7,3.8\r\nSudbury,16841,17659,4.86,153295,2.2,4.7,9.1\r\nSunderland,3777,3684,-2.46,53945,16.1,4.1,10.5\r\nSutton,8250,8963,8.64,105164,1.5,3.5,0.9\r\nSwampscott,14412,13787,-4.34,90763,5.1,4.6,4.8\r\nSwansea,15901,15865,-0.23,68773,4.5,8.9,4\r\nTaunton,55976,55874,-0.18,53600,12.1,7.8,12.3\r\nTempleton,6799,8013,17.86,66138,8.1,6.6,2.7\r\nTewksbury,28851,28961,0.38,84149,2.9,7.2,7.2\r\nTisbury,3755,3949,5.17,58551,4.3,6,15.1\r\nTolland,426,485,13.85,55714,3.4,9.9,0\r\nTopsfield,6141,6085,-0.91,115015,2.4,4.3,2.8\r\nTownsend,9198,8926,-2.96,76533,5.2,6.4,4\r\nTruro,2087,2003,-4.02,80425,8.4,9.5,1\r\nTyngsborough,11081,11292,1.9,95568,4.1,6.1,7.4\r\nTyringham,350,327,-6.57,93750,3.4,4.9,0\r\nUpton,5642,7542,33.68,107950,5.2,6.5,2.4\r\nUxbridge,11156,13457,20.63,81127,6.5,5.3,2.5\r\nWakefield,24804,24932,0.52,89246,2.4,6,4.3\r\nWales,1737,1838,5.81,63800,4.5,6.9,2.8\r\nWalpole,22824,24070,5.46,89697,4.6,6.3,6.1\r\nWaltham,59226,60632,2.37,66346,11.5,5.1,23.7\r\nWare,9707,9872,1.7,51094,13.7,11.4,1.8\r\nWareham,20335,21822,7.31,54451,9,9,8.8\r\nWarren,4776,5135,7.52,55030,8,8.4,2.3\r\nWarwick,750,780,4,67554,5.4,9.4,2.4\r\nWashington,544,538,-1.1,68906,3.2,9.8,3.4\r\nWatertown,32986,31915,-3.25,74081,6.4,5.9,12.4\r\nWayland,13100,12994,-0.81,129805,1.9,4.2,12\r\nWebster,16415,16767,2.14,48640,12.2,10.1,9.7\r\nWellesley,26613,27982,5.14,139784,4.2,5.8,17\r\nWellfleet,2749,2750,0.04,66109,4.2,5,2.2\r\nWendell,986,848,-14,59500,6.3,10.6,7.5\r\nWenham,4440,4875,9.8,132697,3.4,3.6,4.3\r\nWest Boylston,7481,7669,2.51,79906,1.6,7.3,7.2\r\nWest Bridgewater,6634,6916,4.25,76277,5.8,8.3,6.1\r\nWest Brookfield,3804,3701,-2.71,61319,8.5,7.4,4.4\r\nWest Newbury,4149,4235,2.07,111739,3.3,3.2,0\r\nWest Springfield,27899,28391,1.76,51358,12.2,7.1,11.6\r\nWest Stockbridge,1416,1306,-7.77,68750,4.6,4.6,3.4\r\nWest Tisbury,2467,2740,11.07,71667,9.8,6.4,4.4\r\nWestborough,17997,18272,1.53,96069,3.7,4.3,24.4\r\nWestfield,40072,41094,2.55,51620,11.8,6.9,7\r\nWestford,20754,21951,5.77,121168,1.1,6.2,13.2\r\nWesthampton,1468,1607,9.47,81419,5.2,5.5,4.7\r\nWestminster,6907,7277,5.36,79073,4.5,7.4,3.2\r\nWeston,11469,11261,-1.81,148512,4.1,5,12.3\r\nWestport,14183,15532,9.51,68713,4.7,9.8,2.9\r\nWestwood,14117,14618,3.55,114250,3.9,4.9,7.1\r\nWeymouth,53988,53743,-0.45,65849,7,6.4,8.4\r\nWhately,1573,1496,-4.9,74018,4.2,3,4.5\r\nWhitman,13882,14489,4.37,76277,6.4,7.9,5.7\r\nWilbraham,13473,14219,5.54,89336,3.1,6.2,4.4\r\nWilliamsburg,2427,2482,2.27,64545,6.7,2.4,2.1\r\nWilliamstown,8424,7754,-7.95,63045,11.8,6,10.2\r\nWilmington,21363,22325,4.5,94900,2.2,5.7,5.6\r\nWinchendon,9611,10300,7.17,58582,9.8,7.9,5.5\r\nWinchester,20810,21374,2.71,121572,2.5,5.6,10.7\r\nWindsor,875,899,2.74,74750,2.4,2.6,0\r\nWinthrop,18303,17497,-4.4,67535,10.2,6.5,10.4\r\nWoburn,37258,38120,2.31,71060,5.9,6.7,13.5\r\nWorcester,172648,181045,4.86,45036,18.3,8.9,22.6\r\nWorthington,1270,1156,-8.98,61100,7.6,8.1,1.3\r\nWrentham,10554,10955,3.8,94406,3,5.5,3\r\nYarmouth,24807,23793,-4.09,48653,7.9,7.6,5.8\r\nAllston,,29196,,40435,18.7,6.4,33.8\r\nBack Bay,,18088,,83485,2.2,2.5,17.7\r\nBay Village,,1312,,null,null,null,35.1\r\nBeacon Hill,,9023,,82255,4.2,3.2,10.1\r\nBrighton,,45801,,58709,4.9,4.2,25.4\r\nCharlestown,,16439,,83926,16.6,5.8,19.9\r\nChinatown,,4444,,null,null,null,82.5\r\nDorchester,,114235,,41878,13.8,22,73.5\r\nDowntown,,11215,,56461,17.3,6.3,26\r\nEast Boston,,40508,,43511,10.4,8.7,35.2\r\nFenway,,33796,,34438,10.8,8.7,30.4\r\nHarbor Islands,,535,,null,null,37.7,60.7\r\nHyde Park,,30637,,53474,7,9.8,65.2\r\nJamaica Plain,,37468,,65963,11.5,6.1,37.1\r\nLeather District,,639,,null,null,null,20.5\r\nLongwood Medical Area,,3785,,15956,79,14,26.1\r\nMattapan,,22600,,47076,15.1,12.2,91.4\r\nMission Hill,,16305,,36318,20,11.6,45.6\r\nNorth End,,10131,,70277,0.6,2,6.4\r\nRoslindale,,28680,,62913,9.7,7.9,43.1\r\nRoxbury,,48454,,27740,29.2,14.5,81.5\r\nSouth Boston,,33311,,61444,14.3,5.7,19.3\r\nSouth Boston Waterfront,,1889,,76328,0,4.5,10.8\r\nSouth End,,24577,,62267,20.3,9.3,39.1\r\nWest End,,4080,,81397,2.6,3.3,24.8\r\nWest Roxbury,,30446,,71066,6,5.1,22.8\r\n";
        };
        /* 
            Extension to Google Maps to get center of polygon 
            From here: http://code.google.com/p/google-maps-extensions/source/browse/google.maps.Polygon.getBounds.js
            May need this for drawing labels on the shapes


          if (!google.maps.Polygon.prototype.getBounds) {

                  google.maps.Polygon.prototype.getBounds = function(latLng) {

                          var bounds = new google.maps.LatLngBounds();
                          var paths = this.getPaths();
                          var path;
                          
                          for (var p = 0; p < paths.getLength(); p++) {
                                  path = paths.getAt(p);
                                  for (var i = 0; i < path.getLength(); i++) {
                                          bounds.extend(path.getAt(i));
                                  }
                          }

                          return bounds;
                  }

          }*/