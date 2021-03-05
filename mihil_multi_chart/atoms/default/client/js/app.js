import * as d3 from "d3"
// import { container } from "webpack";
import { numberFormat } from './modules/numberFormat'

let target = "#graphicContainer";

function makeCharts(data) {

    console.log(data)

	// d3.select("#chartTitle").text("Changes in prices of essential goods and services, compared to unemployment benefits")

	// d3.select("#subTitle").text("Both CPI data and unemployment benefits have been indexed at 100 in 2011")

	// d3.select("#sourceText").text("| Sources: Australian Bureau of Statistics' Consumer Price Index, Department of Social Services")

	var isMobile;
	var windowWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);

	if (windowWidth < 610) {
			isMobile = true;
	}	

	if (windowWidth >= 610){
			isMobile = false;
	}


    var width = document
    .querySelector("#graphicContainer")
    .getBoundingClientRect().width

    var height = width
    var margin = {top: 20, right: 10, bottom: 20, left:20};

    var numCols
    if (width <= 500) {
        numCols = 2
    } else {
        numCols = 3
    }

    d3.selectAll(".chart-grid").remove()

    var grid_div = d3.select(target)
        .append("div")
        .attr("class", "chart-grid")

	d3.selectAll("#graphicContainer svg").remove();
    
    // CREATE SET OF KEYS FOR THE MULTI LINE
    var line_keys = new Set()
    var variables = data.map(d => d['variable'])

    variables.forEach(variable => line_keys.add(variable))
    line_keys = Array.from(line_keys)

    var everything_else = line_keys.filter(d => d != "UB Index for singles over 21")

    everything_else.forEach(vary => {

        var labels = ["Jobseeker", vary]
        
        var includers = ["UB Index for singles over 21", vary]
   
        var first_init = data.filter(d => includers.includes(d['variable']))
        var init = first_init.filter(d => d['value'] != null)

        let timeParse = d3.timeParse("%Y-%m-%d")
        var init_datto = init.map(d => timeParse(d['Date']))

        var init_grouped = Array.from(d3.group(init, d => d['variable']), 
        ([key, values]) => ({key, values}))

        var color = d3.scaleOrdinal()
            .domain(includers)
            .range(['#e41a1c','#377eb8','#4daf4a','#984ea3',
            '#ff7f00','#ffff33','#a65628','#f781bf','#999999'])
        
        var containerWidth = width / numCols
        var containerHeight = containerWidth * 0.5

        var boxWidth = containerWidth - margin.left - margin.right;
        var boxHeight = containerHeight - margin.top - margin.bottom;

        const x_scale = d3.scaleTime()
            .domain(d3.extent(init_datto))
            .range([margin.left, boxWidth])

        const y_scale = d3.scaleLinear()
            .domain(d3.extent(init.map(d => +d['value'])))
            .range([(boxHeight - margin.bottom), 0])

        var init_div = grid_div.append("div")
            .attr("class", "inline-block")

            var chartKey = init_div.append("div")
            .attr("id", "chartKey")

        var init_svg = init_div.append("svg")
            .style('background-color', "white")
            .attr("class", "init_svg")
            .attr("width", containerWidth)
            .attr("height", containerHeight)


        var features = init_svg.append("g")
            .attr(
                "transform",
                "translate(" + margin.left + "," + margin.top + ")"
              )

        features.append("g")
            .attr("transform", "translate(0," + (boxHeight - margin.bottom) + ")")
            .call(d3.axisBottom(x_scale)
            .ticks(4));

        features.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y_scale)
            .ticks(4));

            // init_svg.append("text")
            // .attr("x", margin.left)
            // .attr("y", (margin.top - 5))
            // .attr("text-anchor", "start")
            // .text(vary)
            // .attr("class", "subTitle")

        features.selectAll(".line")
        .data(init_grouped)
        .enter()
        .append("path")
            .attr("fill", "none")
            .attr("stroke", function(d){ return color(d.key) })
            .attr("stroke-width", 1.5)
            .attr("d", function(d){
                if (function(d) { return d["value"]} != null){
                    return d3.line()
                        .x(function(d) { return x_scale(timeParse(d['Date'])); })
                        .y(function(d) { return y_scale(+d['value']); })
                        (d.values)
                }
            })


        chartKey.append("span")
            .attr("class", "keyText")
            .style("color", color(vary))
            .text(vary)          

        // var varied = init.filter(d => d['variable'] == vary)
        // var ubed = init.filter(d => d['variable'] == "UB Index for singles over 21")

        
        // // console.log("last?", y_scale(varied[varied.length-1]['value']))
        // // console.log("x last?", x_scale(timeParse(ubed[ubed.length-1]['Date'])))

        // features.append("text")
        //     .attr("transform", "translate(" + (x_scale(timeParse(ubed[(ubed.length/2)]['Date']))) + "," + (y_scale(varied[(varied.length/2)]['value']) - 10) + ")")
        //     .attr("dy", ".35em")
        //     .attr("text-anchor", "Middle")
        //     .style("fill", color(vary))
        //     .text(vary);
    
        // features.append("text")
        //     .attr("transform", "translate(" + (x_scale(timeParse(ubed[(ubed.length/2)]['Date']))) + "," + (y_scale(ubed[(ubed.length/2)]['value']) - 10) + ")")
        //     .attr("dy", ".35em")
        //     .attr("text-anchor", "Middle")
        //     .style("fill", color("UB Index for singles over 21"))
        //     .text("Jobseeker");


     //    features.append("text")
     //        .attr("transform", "rotate(-90)")
     //        .attr("y", 25)
     //        // .attr("x", margin.left )
     //        .attr("dy", "0.71em")
     //        .attr("fill", "#767676")
     //        .attr("text-anchor", "end")
     //        .text("Index");

	    // features.append("text")
     //        .attr("x", boxWidth)
     //        .attr("y", boxHeight - margin.bottom - 5)
     //        .attr("fill", "#767676")
     //        .attr("text-anchor", "end")
     //        .text("Date");	

            // if (this.isMobile | !this.lineLabelling) {
            //     this.keys.forEach((key) => {
            //       const $keyDiv = this.$

            var labelColor = d3.scaleOrdinal()
            .domain(labels)
            .range(['#e41a1c','#377eb8','#4daf4a','#984ea3',
            '#ff7f00','#ffff33','#a65628','#f781bf','#999999'])


            
            // var keyDiv = chartKey.append("div")
            //             .attr("class", "keyDiv")
            // labels.forEach(keyer => {
            //     keyDiv.append("span")
            //     .attr("class", "keyCircle")
            //     .style("background-color", () => labelColor(keyer))

            //     keyDiv.append("span")
            //     .attr("class", "keyText")
            //     .text(keyer)
            // })

          
            //       $
            //     })
            //   }




    })


} 

var q = Promise.all([d3.csv("<%= path %>/MIHL_UB_index_pivoted.csv")])

					.then(([data]) => {
						
						makeCharts(data)
						var to=null
						var lastWidth = document.querySelector(target).getBoundingClientRect()
						window.addEventListener('resize', function() {
							var thisWidth = document.querySelector(target).getBoundingClientRect()
							if (lastWidth != thisWidth) {
								window.clearTimeout(to);
								to = window.setTimeout(function() {

                                    makeCharts(data)

									}, 500)
									}
						})
        });