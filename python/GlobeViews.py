import couchdb

def getAllGlobeViews():
    return {
        "_id": "_design/globe",
        "language": "javascript",
        "views": {
            "all_articles": {
                "map": "function(doc) {if (doc['data']['printsection'][0] != 'Sports'){emit(doc['data']['printpagenumber'][0],{neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate']});}}",
            },
            "all_articles_page_1": {
                "map": "function(doc) {if (doc['data']['printsection'][0] != 'Sports' && doc['data']['printpagenumber'] =='1' ){emit(doc['data']['printpublicationdate'][0],{neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate']});}}",                
            },
            "all_articles_by_date": {
                "map": "function(doc) {if (doc['data']['printsection'][0] != 'Sports'){emit(doc['data']['printpublicationdate'][0],{neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate']});}}",                
            },
            "city_count": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA' && doc['data']['printsection'][0] != 'Sports'){  emit([doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "city_count_page_1": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpagenumber'] =='1' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA' && doc['data']['printsection'][0] != 'Sports'){  emit([doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "city_count_today": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpublicationdate'] =='20121021' && doc['data']['printpagenumber'] =='1' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA' && doc['data']['printsection'][0] != 'Sports'){  emit([doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "headline_by_city": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'][0] =='MA' && doc['data']['printsection'][0] != 'Sports'){  emit(doc['data']['city'][0],{canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],printpagenumber:doc['data']['printpagenumber'][0],state:doc['data']['state'][0]});}}",                
            },
            "headline_by_city_page_1": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpagenumber'] =='1' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'][0] =='MA' && doc['data']['printsection'][0] != 'Sports'){  emit(doc['data']['city'][0],{canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],printpagenumber:doc['data']['printpagenumber'][0],state:doc['data']['state'][0]});}}",                
            },
            "headline_by_city_today": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpublicationdate'] =='20121021' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'][0] =='MA' && doc['data']['printsection'][0] != 'Sports'){  emit(doc['data']['city'][0],{canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],printpagenumber:doc['data']['printpagenumber'][0],state:doc['data']['state'][0]});}}",                
            },
            "headline_by_neighborhood": {
                "map": "function(doc) {if(doc['data']['neighborhood'] != null && doc['data']['neighborhood'].length > 0  && doc['data']['printsection'][0] != 'Sports'){  emit(doc['data']['neighborhood'],  { canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],    printpagenumber:doc['data']['printpagenumber'][0]  });}}",                
            },
            "headline_by_neighborhood_page_1": {
                "map": "function(doc) {if(doc['data']['neighborhood'] != null && doc['data']['printpagenumber'] =='1' && doc['data']['neighborhood'].length > 0  && doc['data']['printsection'][0] != 'Sports'){  emit(doc['data']['neighborhood'],  { canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],    printpagenumber:doc['data']['printpagenumber'][0]  });}}",                
            },
            "headline_by_neighborhood_today": {
                "map": "function(doc) {if(doc['data']['neighborhood'] != null && doc['data']['printpublicationdate'] =='20121021' && doc['data']['neighborhood'].length > 0  && doc['data']['printsection'][0] != 'Sports'){  emit(doc['data']['neighborhood'],  { canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],    printpagenumber:doc['data']['printpagenumber'][0]  });}}",                
            },
            "metadata": {
                "map": "function(doc) { if (doc['type']=='metadata'){        emit(doc,1);        }}",                
            },
            

           
        }, 
    }