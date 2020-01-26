import React, { Component } from 'react'
import { geoMercator, geoPath } from 'd3-geo'
import * as d3 from 'd3';
import * as d3geo from 'd3-geo';
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

    componentDidMount(){
        const {height, width, counties, loading} = this.state;

        //https://bl.ocks.org/mbostock/4707858

        // create SVG
        const svg = d3.select(this.refs.canvas)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .style("border", "1px solid black");

        
        d3.json("http://127.0.0.1:5000/static/storage/us.json")
        .then(function(us){


                // Create a unit projection.
            var projection = d3.geoAlbers()
                .scale(1)
                .translate([0, 0]);

            console.log(us)
            // Append empty placeholder g element to the SVG
            // g will contain geometry elements
            let g = svg.append( "g" );

            // Create GeoPath function that uses built-in D3 functionality to turn
            // lat/lon coordinates into screen coordinates
            let us_geoPath = d3.geoPath().projection(projection);

            var states = topojson.feature(us, us.objects.states),
                state = states.features.filter(function(d) { return d.id === 6; })[0];

            // Compute the bounds of a feature of interest, then derive scale & translate.
            var b = us_geoPath.bounds(state),
                s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height),
                t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

            // Update the projection to use computed scale & translate.
            projection
                .scale(s)
                .translate(t);
                
            svg.append("path")
                .datum(states)
                .attr("class", "feature")
                .attr("d", us_geoPath);
          
            svg.append("path")
                .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
                .attr("class", "mesh")
                .attr("d", us_geoPath);

            svg.append("path")
                .datum(topojson.mesh(us, us.objects.counties))
                .attr("class", "mesh")
                .attr("d", us_geoPath);
          
            svg.append("path")
                .datum(state)
                .attr("class", "outline")
                .attr("d", us_geoPath);
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
        return <div ref="canvas"></div>
    }
}
export default USMap