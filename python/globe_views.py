import couchdb

def getAllGlobeViews():
    return {
        "_id": "_design/globe",
        "language": "javascript",
        "views": {
            "all_articles": {
                "map": "function(doc) {emit(doc['data']['printpagenumber'][0],{neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate'],canonicalurl:doc['data']['canonicalurl']});}",
            },
            "all_articles_page_1": {
                "map": "function(doc) { if(doc['data']['printpagenumber'] == 1){ emit(doc['data']['printpublicationdate'][0], {neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate'],canonicalurl:doc['data']['canonicalurl']})};}",
            },
            "all_articles_by_date": {
                "map": "function(doc) { emit(doc['data']['printpublicationdate'][0],{neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate'],canonicalurl:doc['data']['canonicalurl']});}",
            },
            "city_count": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA'){  emit([doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "city_count_page_1": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpagenumber'] =='1' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA'){  emit([doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "city_count_yesterday": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA'){  emit([doc['data']['printpublicationdate'][0],doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "city_count_printsection": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'] =='MA'){  emit([doc['data']['printsection'][0], doc['data']['city'][0], doc['data']['neighborhood']] ,1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "headline_by_city": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'][0] =='MA' ){  emit(doc['data']['city'][0],{canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],printpagenumber:doc['data']['printpagenumber'][0],state:doc['data']['state'][0]});}}",
            },
            "headline_by_city_page_1": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpagenumber'] =='1' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'][0] =='MA'){  emit(doc['data']['city'][0],{canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],printpagenumber:doc['data']['printpagenumber'][0],state:doc['data']['state'][0]});}}",
            },
            "headline_by_city_today": {
                "map": "function(doc) {if(doc['data']['city'] != null && doc['data']['printpublicationdate'] =='20121021' && doc['data']['city'].length > 0 && doc['data']['state'].length > 0 && doc['data']['state'][0] =='MA'){  emit(doc['data']['city'][0],{canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],printpagenumber:doc['data']['printpagenumber'][0],state:doc['data']['state'][0]});}}",
            },
            "headline_by_neighborhood": {
                "map": "function(doc) {if(doc['data']['neighborhood'] != null && doc['data']['neighborhood'].length > 0 ){  emit(doc['data']['neighborhood'],  { canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],    printpagenumber:doc['data']['printpagenumber'][0]  });}}",
            },
            "headline_by_neighborhood_page_1": {
                "map": "function(doc) {if(doc['data']['neighborhood'] != null && doc['data']['printpagenumber'] =='1' && doc['data']['neighborhood'].length > 0 ){  emit(doc['data']['neighborhood'],  { canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],    printpagenumber:doc['data']['printpagenumber'][0]  });}}",
            },
            "headline_by_neighborhood_today": {
                "map": "function(doc) {if(doc['data']['neighborhood'] != null && doc['data']['printpublicationdate'] =='20121021' && doc['data']['neighborhood'].length > 0 ){  emit(doc['data']['neighborhood'],  { canonicalurl:doc['data']['canonicalurl'][0],headline:doc['data']['headline'][0],    printpagenumber:doc['data']['printpagenumber'][0]  });}}",
            },
            "metadata": {
                "map": "function(doc) { if (doc['type']=='metadata'){       emit(doc['last_article_date'],doc);           }}",
            },
            "last_article_date": {
                "map": "function(doc) { if (doc['type']=='metadata'){        emit(doc['type'],doc['last_article_date'][0]);        }}",
            },
            "doc_by_canonical_url": {
                "map": "function(doc) {emit(doc['data']['canonicalurl'][0],doc)}",
            },
            "doc_by_uuid": {
                "map": "function(doc) {emit(doc['data']['uuid'][0],doc)}",
            },
            "all_articles_by_printsection": {
                "map": "function(doc) {emit(doc['data']['printsection'][0],{neighborhood:doc['data']['neighborhood'],headline:doc['data']['headline'],printbook:doc['data']['printbook'],summary:doc['data']['summary'],city:doc['data']['city'],latitude:doc['data']['latitude'],longitude:doc['data']['longitude'],printsection:doc['data']['printsection'],printpagenumber:doc['data']['printpagenumber'],wordcount:doc['data']['wordcount'],printpublicationdate:doc['data']['printpublicationdate'],canonicalurl:doc['data']['canonicalurl']});}",
            },
            
           
        },
    }
def getNLTKViews():
    return {
         "_id": "_design/nltk",
        "language": "javascript",
        "views": {


            "fulltext_by_city_or_neighborhood": {
                "map": "function(doc) {  if (doc.type=='article' && doc.data.neighborhood != '' && doc.data.state[0] =='MA'){ emit(doc.data.neighborhood, doc.data.fulltext); } else if(doc.type=='article' && doc.data.state[0] =='MA'){ emit(doc.data.city[0], doc.data.fulltext); }}",
            },
            #function(doc) { if (doc.type=='article' && doc.data.neighborhood != ''){    emit([doc.data.neighborhood, doc.data.state[0]], 1); } else if(doc.type=='article' && doc.data.city !=''){emit( [doc.data.city[0],doc.data.state[0]], 1);}}
            "cities_or_neighborhoods": {
                "map": "function(doc) { if (doc.type=='article' && doc.data.neighborhood != ''){    emit(doc.data.neighborhood, 1); } else if(doc.type=='article' && doc.data.city !=''){emit(doc.data.city[0], 1);}}",
                "reduce": "function(keys, values) { return sum(values); }",
            },
            "place_frequency": {
                "map": "function(doc) {if(doc.type=='place_frequency'){emit([doc.city_or_neighborhood, doc.date], doc);}}",                
            },
            "frequency_by_place": {
                "map": "function(doc) {if(doc.type=='place_frequency'){if(doc.freqdist.length > 0) {for(var entry in doc.freqdist) {emit(doc.freqdist[entry][0], {'place':doc.city_or_neighborhood, 'frequency': doc.freqdist[entry][1] });}}}}",                
            },
            
        }
    }
