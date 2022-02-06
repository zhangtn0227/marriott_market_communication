d3.queue()
    .defer(MiniApp_linechart_func,MiniApp_lineChartDataUrl)
    .defer(MiniApp_piechart_func,MiniApp_pieChartDataUrl)
    .defer(ZKT_linechart_func,ZKT_lineChartDataUrl)
    .defer(ZKT_piechart_func,ZKT_pieChartDataUrl)
    .defer(MTDP_linechart_func,MTDP_lineChartDataUrl)
    .defer(MTDP_piechart_func,MTDP_pieChartDataUrl)

    .await(function(error){
        if(error) throw error;
        console.log("There is a error");
    })


function MiniApp_piechart_func(pieChartDataUrl) {
    

    // Create dummy data
    d3.json(pieChartDataUrl, function(error, d){


        var tooltip = d3.select("#Miniapp_pieChart")
		.append('div')
		.attr('class', 'tooltip');

		tooltip.append('div')
		.attr('class', 'item');

		tooltip.append('div')
		.attr('class', 'revenue');

		tooltip.append('div')
		.attr('class', 'percent');

        var data ={};
        var percentage_dic = {};
        var revenueMin = 0;
        var revenueMax = 0;
        var total_revenue = 0;
        for (var i = 0; i <d.length; i++){
 
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            total_revenue = total_revenue + value;
            revenueMin = Math.min(revenueMin,value);
            revenueMax = Math.max(revenueMax,value);
            data[obj] = value;
        }

        for (var i =0; i < d.length;i++){
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            percentage_dic[obj] = value / total_revenue;
        }

        console.log(data);
 

        // set the dimensions and margins of the graph
        var width = 270
        var height = 270
        var margin = 5
        var donutWidth = 40
        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        var radius = Math.min(width, height) / 2 - margin
        // append the svg object to the div called 'my_dataviz'
        var svg = d3.select("#Miniapp_pieChart")
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
        var pie = d3.layout.pie().sort(null)
        .value(function(d) {return d.value; })

        var data_ready = pie(d3.entries(data))
        // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
        var path = svg
        .selectAll('path')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', d3.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius)
        )
        .attr('fill', function(d,i){ return(color(i)); })
        .attr("stroke", "black")
        .each(function(d){ this._current = d;})
        .style("stroke-width", "2px")
        .style("opacity", 0.7)

        path.on('mouseover', function(percentage_dic) {
            console.log(percentage_dic)
			var percent = Math.round(1000 * percentage_dic.value / total_revenue) / 10;
			tooltip.select('.item').html(percentage_dic.data.key).style('color','black');
			tooltip.select('.revenue').html(percentage_dic.revenue);
			tooltip.select('.percent').html(percentage_dic.data.key+" revenue "+percentage_dic.value +" per "+ percent+'%');
			tooltip.style('display', 'block');
			tooltip.style('opacity',4);

		});


		path.on('mousemove', function(d) {
			tooltip.style('top', (d3.event.layerY + 10) + 'px')
			.style('left', (d3.event.layerX - 25) + 'px');
		});

		path.on('mouseout', function() {
			tooltip.style('display', 'none');
			tooltip.style('opacity',0);
		});


    });
    
}
function ZKT_piechart_func(pieChartDataUrl) {
    

    // Create dummy data
    d3.json(pieChartDataUrl, function(error, d){


        var tooltip = d3.select("#ZKT_pieChart")
		.append('div')
		.attr('class', 'tooltip');

		tooltip.append('div')
		.attr('class', 'item');

		tooltip.append('div')
		.attr('class', 'revenue');

		tooltip.append('div')
		.attr('class', 'percent');

        var data ={};
        var percentage_dic = {};
        var revenueMin = 0;
        var revenueMax = 0;
        var total_revenue = 0;
        for (var i = 0; i <d.length; i++){
 
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            total_revenue = total_revenue + value;
            revenueMin = Math.min(revenueMin,value);
            revenueMax = Math.max(revenueMax,value);
            data[obj] = value;
        }

        for (var i =0; i < d.length;i++){
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            percentage_dic[obj] = value / total_revenue;
        }

        console.log(data);
 

        // set the dimensions and margins of the graph
        var width = 270
        var height = 270
        var margin = 5
        var donutWidth = 40
        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        var radius = Math.min(width, height) / 2 - margin
        // append the svg object to the div called 'my_dataviz'
        var svg = d3.select("#ZKT_pieChart")
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
        var pie = d3.layout.pie().sort(null)
        .value(function(d) {return d.value; })

        var data_ready = pie(d3.entries(data))
        // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
        var path = svg
        .selectAll('path')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', d3.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius)
        )
        .attr('fill', function(d,i){ return(color(i)); })
        .attr("stroke", "black")
        .each(function(d){ this._current = d;})
        .style("stroke-width", "2px")
        .style("opacity", 0.7)

        path.on('mouseover', function(percentage_dic) {
            console.log(percentage_dic)
			var percent = Math.round(1000 * percentage_dic.value / total_revenue) / 10;
			tooltip.select('.item').html(percentage_dic.data.key).style('color','black');
			tooltip.select('.revenue').html(percentage_dic.revenue);
			tooltip.select('.percent').html(percentage_dic.data.key+" revenue "+percentage_dic.value +" per "+ percent+'%');
			tooltip.style('display', 'block');
			tooltip.style('opacity',4);

		});


		path.on('mousemove', function(d) {
			tooltip.style('top', (d3.event.layerY + 10) + 'px')
			.style('left', (d3.event.layerX - 25) + 'px');
		});

		path.on('mouseout', function() {
			tooltip.style('display', 'none');
			tooltip.style('opacity',0);
		});


    });
    
}
function MTDP_piechart_func(pieChartDataUrl) {
    

    // Create dummy data
    d3.json(pieChartDataUrl, function(error, d){


        var tooltip = d3.select("#MTDP_pieChart")
		.append('div')
		.attr('class', 'tooltip');

		tooltip.append('div')
		.attr('class', 'item');

		tooltip.append('div')
		.attr('class', 'revenue');

		tooltip.append('div')
		.attr('class', 'percent');

        var data ={};
        var percentage_dic = {};
        var revenueMin = 0;
        var revenueMax = 0;
        var total_revenue = 0;
        for (var i = 0; i <d.length; i++){
 
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            total_revenue = total_revenue + value;
            revenueMin = Math.min(revenueMin,value);
            revenueMax = Math.max(revenueMax,value);
            data[obj] = value;
        }

        for (var i =0; i < d.length;i++){
            var obj = d[i]["item"];
            var value =  parseFloat(d[i]["revenue"]);
            percentage_dic[obj] = value / total_revenue;
        }

        console.log(data);
 

        // set the dimensions and margins of the graph
        var width = 270
        var height = 270
        var margin = 5
        var donutWidth = 40
        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        var radius = Math.min(width, height) / 2 - margin
        // append the svg object to the div called 'my_dataviz'
        var svg = d3.select("#MTDP_pieChart")
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
        var pie = d3.layout.pie().sort(null)
        .value(function(d) {return d.value; })

        var data_ready = pie(d3.entries(data))
        // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
        var path = svg
        .selectAll('path')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', d3.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius)
        )
        .attr('fill', function(d,i){ return(color(i)); })
        .attr("stroke", "black")
        .each(function(d){ this._current = d;})
        .style("stroke-width", "2px")
        .style("opacity", 0.7)

        path.on('mouseover', function(percentage_dic) {
            console.log(percentage_dic)
			var percent = Math.round(1000 * percentage_dic.value / total_revenue) / 10;
			tooltip.select('.item').html(percentage_dic.data.key).style('color','black');
			tooltip.select('.revenue').html(percentage_dic.revenue);
			tooltip.select('.percent').html(percentage_dic.data.key+" revenue "+percentage_dic.value +" per "+ percent+'%');
			tooltip.style('display', 'block');
			tooltip.style('opacity',4);

		});


		path.on('mousemove', function(d) {
			tooltip.style('top', (d3.event.layerY + 10) + 'px')
			.style('left', (d3.event.layerX - 25) + 'px');
		});

		path.on('mouseout', function() {
			tooltip.style('display', 'none');
			tooltip.style('opacity',0);
		});


    });
    
}

function MiniApp_linechart_func(lineChartDataUrl) {
    //Read the data
    d3.json(lineChartDataUrl,

        // When reading the csv, I must format variables:
        function(d){
            console.log("in d function");
                // set the dimensions and margins of the graph
            var margin = {top: 20, right: 20, bottom: 20, left: 40},
            width = 500 - margin.left - margin.right,
            height = 360 - margin.top - margin.bottom;
            console.log("we are in read function ")
            // append the svg object to the body of the page
            var svg = d3.select("#Miniapp_lineChart")
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

function ZKT_linechart_func(lineChartDataUrl) {


    //Read the data
    d3.json(lineChartDataUrl,

    // When reading the csv, I must format variables:
    function(d){
        console.log("in d function");
            // set the dimensions and margins of the graph
        var margin = {top: 20, right: 20, bottom: 20, left: 40},
        width = 500 - margin.left - margin.right,
        height = 360 - margin.top - margin.bottom;
        console.log("we are in read function ")
        // append the svg object to the body of the page
        var svg = d3.select("#ZKT_lineChart")
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
function MTDP_linechart_func(lineChartDataUrl) {


    //Read the data
    d3.json(lineChartDataUrl,

    // When reading the csv, I must format variables:
    function(d){
        console.log("in d function");
            // set the dimensions and margins of the graph
        var margin = {top: 20, right: 20, bottom: 20, left: 40},
        width = 500 - margin.left - margin.right,
        height = 360 - margin.top - margin.bottom;
        console.log("we are in read function ")
        // append the svg object to the body of the page
        var svg = d3.select("#MTDP_lineChart")
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


