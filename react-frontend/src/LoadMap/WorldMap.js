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
            height: 800,
            width: 800,
            counties: this.props.counties,
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

        d3.json('https://gist.githubusercontent.com/jdev42092/5c285c4a3608eb9f9864f5da27db4e49/raw/a1c33b1432ca2948f14f656cc14c7c7335f78d95/boston_neighborhoods.json')
        .then(function(data){
            console.log(data)
            // Append empty placeholder g element to the SVG
            // g will contain geometry elements
            let g = svg.append( "g" );
    
            // define math projection a.k.a where it starts
            let usProjection = d3.geoAlbers()
                .scale( 190000 )
                .rotate( [71.057,0] )
                .center( [0, 42.313] )
                .translate( [width/2,height/2] );
    
            // Create GeoPath function that uses built-in D3 functionality to turn
            // lat/lon coordinates into screen coordinates
            let us_geoPath = d3.geoPath()
                .projection( usProjection );
            
    
            // Classic D3... Select non-existent elements, bind the data, append the elements, and apply attributes
            g.selectAll( "path" )
                .data( data.features )
                .enter()
                .append( "path" )
                .attr( "fill", "#ccc" )
                .attr( "stroke", "#333")
                .attr( "d", us_geoPath );
    
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