import React, { Component } from 'react'
import { geoMercator, geoPath } from 'd3-geo'
import * as d3 from 'd3';
import axios from 'axios';
import * as topojson from "topojson";
import './USMap.scss';



class USMap extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            height: 600,
            width: 960,
            loading: true
        };
    }

    // http://bl.ocks.org/threestory/ed0f322d7bb2e3be8ded
    componentDidMount(){
        const {height, width, counties, loading} = this.state;
			var w = width;
			var h = height;

			//Define map projection
			var projection = d3.geoMercator()
            .center([ -120, 37 ])
            .translate([ w/2, h/2 ])
            .scale([ w*3.3 ]);

			var path = d3.geoPath().projection(projection);
			

			//Create SVG
			var svg = d3.select(this.refs.canvas)
						.append("svg")
						.attr("width", w)
                        .attr("height", h)
                        .style("border", "1px solid black");

			//Load in GeoJSON data
			d3.json("http://127.0.0.1:5000/static/storage/cb_2014_us_county_5m.json").then(function(json) {
                console.log(json);


				//Bind data and create one path per GeoJSON feature
				svg.selectAll("path")
					.data(json.features)
					.enter()
					.append("path")
					.attr("d", path)
				   	.on("mouseover", function(d){
                        console.log(d.properties.NAME)
						var xPosition = w/2 + 150;
						var yPosition = h/2;
// 						var xPosition = parseFloat(path.centroid(this).attr("cx"));
// 						var yPosition = parseFloat(path.centroid(this).attr("cy"));
                        d3.select("#tooltip")
                            .style("left", xPosition + "px")
                            .style("top", yPosition + "px");
                        d3.select("#county")
						    .text(d.properties.NAME);
						d3.select("#tooltip")
						    .classed("hidden", false);
						})
                    .on("mouseout", function(){
                    d3.select("#tooltip").classed("hidden", true);
                    });
		
			});
    }

    componentdfdfDidMount(){
        const {height, width, counties, loading} = this.state;

        //https://bl.ocks.org/mbostock/4707858

        // create SVG
        const svg = d3.select(this.refs.canvas)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .style("border", "1px solid black");

        
        d3.json("http://127.0.0.1:5000/static/storage/california_06_counties.json")
        .then(function(us){


            // Create a unit projection.
            var projection = d3.geoAlbers()
                .scale(1)
                .translate([0, 0]);

            console.log(us)
            // Create GeoPath function that uses built-in D3 functionality to turn
            // lat/lon coordinates into screen coordinates
            let us_geoPath = d3.geoPath().projection(projection);

            var california = topojson.feature(us, us.objects.cb_2015_california_county_20m)

            // Compute the bounds of a feature of interest, then derive scale & translate.
            var b = us_geoPath.bounds(california),
                s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
                t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

            // Update the projection to use computed scale & translate.
            projection
                .scale(s)
                .translate(t);
                
            svg.append("path")
                .datum(california)
                .attr("class", "feature")
                .attr("d", us_geoPath);
/*
             // "land" from merged counties
            const land = svg.append("g")
            .attr("id", "land")
            .append("path")
            .datum(landArea)
            .attr("fill", "white")
            .attr("stroke-width", 1.25)
            .attr("stroke", 'white')
            .attr("stroke-line-join", "round")
            .attr("d", path)

            const countiesGroup = svg.append("g").attr("id", "county-boundaries")
               
            countiesGroup.selectAll('.county')
            .data(countyFeats.features)
            .enter()
            .append('path')
            .attr("stroke-width", 1.25)
            .attr("stroke", 'white')
            .attr('d', path)
            .attr("fill", d => data.get(d.properties.GEOID) ? color(data.get(d.properties.GEOID)) : "#eee")    
            .on('mouseover', mouseover)
            .on('mouseout', mouseout)*/

            svg.selectAll(".county")
                //.data(countyFeats.features)
                .enter()
                .append("path")
                .attr("stroke-width", 1.25)
                .attr("stroke", 'white')
                .attr('d', us_geoPath) 
                .on("mouseover", function (d){
                    console.log("Hovered", d);
                    svg.transition()    
                        .duration(200)    
                        .style("opacity", .9);    
                    svg.html(california.get(d.properties.GEOID))  
                        .style("left", (d3.event.pageX) + "px")   
                        .style("top", (d3.event.pageY - 28) + "px");  
                })
                .on("mouseout", function (d){
                    svg.transition()    
                        .duration(500)    
                        .style("opacity", 0); 
                });

           /* // county boundaries
            const countiesGroup = svg.append("path").attr("id", "county-boundaries")
            
            countiesGroup.selectAll('.county')
                .data(us.objects.cb_2015_california_county_20m)
                .enter()
                .append('path')
                .attr("stroke-width", 1.25)
                .attr("stroke", 'white')
                .attr('d', us_geoPath)
                .on("mouseover", function (d){
                    console.log("Hovered");
                    svg.html("County ID "); 
                })
                .on("mouseout", function (d){
                    svg.transition()    
                        .duration(500)    
                        .style("opacity", 0); 
                });*/
                

                

        })
        

/*
        // define math projection
        // define path generator
        const path = d3.geoPath()
        const projection = d3.geoAlbersUsa().scale(1300).translate([487.5, 305])
        

        console.log(counties)

        // load in GeoJSON data
        d3.json("./zipcode-data", function(json) {
            console.log(json)
            svgCanvas.selectAll("path")
                .data(topojson.feature(topojson.mesh(json, json.objects.counties, (a, b) => a !== b && (a.id / 1000 | 0) === (b.id / 1000 | 0))))
                .enter()
                .append("path")
        })*/

    }
    

    render() {
        return( 
        <div><div ref="canvas"></div>
            <p>County: <span id="county">County Name</span></p>
        </div>)
    }
}
export default USMap