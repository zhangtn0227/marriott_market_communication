d3.queue()
    .defer(linechart_func,lineChartDataUrl)
    .defer(piechart_func,pieChartDataUrl)
    .await(function(error){
        if(error) throw error;
        console.log("There is a error");
    })


function piechart_func(pieChartDataUrl) {
    

    // Create dummy data
    d3.json(pieChartDataUrl, function(error, d){
        var data ={};
        var revenueMin = 0;
        var revenueMax = 0;
        for (var i = 0; i <d.length; i++){
 
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            revenueMin = Math.min(revenueMin,value);
            revenueMax = Math.max(revenueMax,value);
            data[obj] = value;
        }
        console.log(data);
 

        // set the dimensions and margins of the graph
        var width = 270
        height = 270
        margin = 5
        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        var radius = Math.min(width, height) / 2 - margin
        // append the svg object to the div called 'my_dataviz'
        var svg = d3.select("#pieChart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
        
        // set the color scale
        var color = d3.scaleLinear().domain([1,d.length])
        .range(["#fff", "#3B73B4"]);

        console.log(color);
        // Compute the position of each group on the pie:
        var pie = d3.pie()
        .value(function(d) {return d.value; })

        var data_ready = pie(d3.entries(data))
        // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
        svg
        .selectAll('whatever')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', d3.arc()
        .innerRadius(0)
        .outerRadius(radius)
        )
        .attr('fill', function(d,i){ return(color(i)); })
        .attr("stroke", "black")
        .style("stroke-width", "2px")
        .style("opacity", 0.7)

        svg
        .selectAll('mySlices')
        .data(data_ready)
        .enter()
        .append('text')
        .text(function(d){ return "grp " + d.data.key})
        .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
        .style("text-anchor", "middle")
        .style("font-size", 17)
});
    
}

function linechart_func(lineChartDataUrl) {


    //Read the data
    d3.json(lineChartDataUrl,

    // When reading the csv, I must format variables:
    function(d){
        console.log("in d function");
            // set the dimensions and margins of the graph
        var margin = {top: 10, right: 10, bottom: 10, left: 10},
        width = 500 - margin.left - margin.right,
        height = 360 - margin.top - margin.bottom;
        console.log("we are in read function ")
        // append the svg object to the body of the page
        var svg = d3.select("#lineChart")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
 
        // Add X axis --> it is a date format
        var x = d3.scaleTime()
        .domain(d3.extent(d, function(d) { return d3.timeParse("%Y-%m-%d")(d.date); }))
        .range([ 0, width ]);
        svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));
  
        // Add Y axis
        var y = d3.scaleLinear()
        .domain([0, d3.max(d, function(d) { return +d.revenue; })])
        .range([ height, 0 ]);
        svg.append("g")
        .call(d3.axisLeft(y));

        // Add the line
        svg.append("path")
        .datum(d)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function(d) { return x(d3.timeParse("%Y-%m-%d")(d.date)) })
            .y(function(d) { return y(d.revenue) })
            )
        });
   
    // Now I can use this dataset:
    
}