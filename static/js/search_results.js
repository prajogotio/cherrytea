// Loading Images of Results

function loadSearchImages( srcArray ){
    
    srcArray.forEach(function (entry){
        
        var img_src = " <img src=\"{{ url_for('static', filename='img/   " + entry + " ') }} \">   ";
        $(".search_results").append(img_src);
    
    });
    
}



// Search Query

function search_clicked(){

    var search_query = $("#search_bar").val();
    console.log(search_query);
}

