import React, { Component } from 'react'
import { geoMercator, geoPath } from 'd3-geo'
import * as d3 from 'd3';
import * as d3geo from 'd3-geo';
import axios from 'axios';
import * as topojson from "topojson";



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


        // create SVG
        const svg = d3.select(this.refs.canvas)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .style("border", "1px solid black");

        d3.json("http://127.0.0.1:5000/static/storage/counties-albers-10m.json")
        .then(function(us){
            console.log(us)
            // Append empty placeholder g element to the SVG
            // g will contain geometry elements
            let g = svg.append( "g" );

            // Create GeoPath function that uses built-in D3 functionality to turn
            // lat/lon coordinates into screen coordinates
            let us_geoPath = d3.geoPath();
            
    
            // Classic D3... Select non-existent elements, bind the data, append the elements, and apply attributes
            g.selectAll("path")
                .data(topojson.feature(us, us.objects.counties).features) // Bind TopoJSON data elements
            // pass through what objects you want to use -- in this case we are doing county lines
                .enter().append("path")
                .attr("d", us_geoPath)
                .style("fill", "white")
                .style("stroke", "black");
    
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