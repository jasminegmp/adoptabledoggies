import React, { Component } from 'react'
import * as d3 from 'd3';
import axios from 'axios';
import './USMap.scss';


class USMap extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            height: 600,
            width: 650,
            loading: true,
            county: null
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
                //console.log(json);

				//Bind data and create one path per GeoJSON feature
				svg.selectAll("path")
					.data(json.features)
					.enter()
					.append("path")
                    .attr("d", path)
                    //.attr("fill",function(d) {console.log(d.properties.NAME); if (d.properties.NAME === "Los Angeles") { console.log(d.properties.NAME);return "red"}})
                    .style("fill", function(d){
                        if (d.properties.NAME === "Los Angeles" || d.properties.NAME === "Orange" || d.properties.NAME === "Ventura" || d.properties.NAME === "Imperial" || d.properties.NAME === "San Diego" || d.properties.NAME === "San Bernardino" || d.properties.NAME === "Riverside"){
                            //console.log(d.properties.NAME)
                            return "#2a9d8f"
                        }
                    })   
                    .on("click", function(d){
                        if (d.properties.NAME === "Los Angeles" || d.properties.NAME === "Orange" || d.properties.NAME === "Ventura" || d.properties.NAME === "Imperial" || d.properties.NAME === "San Diego" || d.properties.NAME === "San Bernardino" || d.properties.NAME === "Riverside"){
                            //console.log(d.properties.NAME)
                            d3.select("#county")
                                .text(d.properties.NAME);
                            d3.select("#tooltip")
                                .classed("hidden", false);
                            d3.select(this).style("fill", "#e9c46a");
                        }
                    })  
                    .on("mouseout", function(d){
                        if (d.properties.NAME === "Los Angeles" || d.properties.NAME === "Orange" || d.properties.NAME === "Ventura" || d.properties.NAME === "Imperial" || d.properties.NAME === "San Diego" || d.properties.NAME === "San Bernardino" || d.properties.NAME === "Riverside"){
                            d3.select(this).style("fill", "#2a9d8f");
                        }
                        else{
                            d3.select(this).style("fill", "#264653");
                        }
                    }) 
                    
            });
                
		
	    }


    render() {
        return( 
        <div><div ref="canvas"></div>
            <p>County: <span id="county">County Name</span></p>
        </div>)
    }
}
export default USMap