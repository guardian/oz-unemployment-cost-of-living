import * as d3 from "d3"
// import { container } from "webpack";
import { numberFormat } from './modules/numberFormat'

let target = "#graphicContainer";

function makeCharts(data) {

    console.log("data", data)
    var nuColumns = 2;

	d3.select("#chartTitle").text("China dominates Pacific extractive exports")

	d3.select("#subTitle").text("Value of trade flows measured in tonnes")

	d3.select("#sourceText").text("| Guardian analysis of CEPII's BACI dataset")

	var isMobile;
	var windowWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);

	if (windowWidth < 610) {
			isMobile = true;
	}	

	if (windowWidth >= 610){
			isMobile = false;
	}

	var width = document.querySelector(target).getBoundingClientRect().width
	var height = width*0.45;					
	var margin = {top: 20, right: 10, bottom: 20, left:30};

	width = width - margin.left - margin.right,
    height = height - margin.top - margin.bottom;


	d3.select("#graphicContainer svg").remove();
    d3.selectAll(".init_svg svg").remove();

    // CREATE SET OF KEYS FOR THE MULTI LINE
    var line_keys = new Set()
    var variables = data.map(d => d['variable'])

    variables.forEach(variable => line_keys.add(variable))
    line_keys = Array.from(line_keys)

    var everything_else = line_keys.filter(d => d != "UB Index for singles over 21")

    everything_else.forEach(vary => {
        
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
        
        var containerWidth = width / nuColumns
        var containerHeight = containerWidth * 0.5

        var boxWidth = containerWidth - margin.left - margin.right;
        var boxHeight = containerHeight - margin.top - margin.bottom;

        const x_scale = d3.scaleTime()
            .domain(d3.extent(init_datto))
            .range([0, boxWidth])

        const y_scale = d3.scaleLinear()
            .domain(d3.extent(init.map(d => +d['value'])))
            .range([boxHeight, 0])

        var target_div = d3.select(target)

        var init_div = target_div.append("div")
            .attr("class", "chart-grid inline-block")

        var init_svg = init_div.append("svg")
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
            .call(d3.axisBottom(x_scale).ticks(5));



        features.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y_scale));

        features.selectAll(".line")
        .data(init_grouped)
        .enter()
        .append("path")
            .attr("fill", "none")
            .attr("stroke", function(d){ return color(d.key) })
            .attr("stroke-width", 1.5)
            .attr("d", function(d){
                console.log(d)
                if (function(d) { return d["value"]} != null){
                    return d3.line()
                        .x(function(d) { return x_scale(timeParse(d['Date'])); })
                        .y(function(d) { return y_scale(+d['value']); })
                        (d.values)
                }
            })


    })


} 

var q = Promise.all([d3.csv("<%= path %>/selected_cpi_ub_PIVOTED.csv")])

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