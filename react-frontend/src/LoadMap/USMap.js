import React, { Component } from 'react'
import * as d3 from 'd3';
import axios from 'axios';
import './USMap.scss';


class USMap extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            height: 600,
            width: 960,
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
				   	.on("mouseover", function(d){
                        //console.log(d.properties.NAME)
                        d3.select("#county")
						    .text(d.properties.NAME);
						d3.select("#tooltip")
                            .classed("hidden", false);
                        this.setState({county: d.properties.NAME})
                        })
                        
                    .on("mouseout", function(){
                    d3.select("#tooltip").classed("hidden", true);
                    
            });
                
		
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