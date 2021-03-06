import React, { Component } from 'react'
import * as d3 from 'd3';
import './USMap.scss';
import CountyInfo from '../CountyInfo/index';


class USMap extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            height: 550,
            width: 550,
            loading: true,
            county: null,
            prevCounty: null,
            prevCountyObj: null
        };
    }

    countyCalled = (county) =>{
        this.setState({ prevCounty: this.state.county});
        this.setState({county});
    }

    // http://bl.ocks.org/threestory/ed0f322d7bb2e3be8ded
    componentDidMount(){
        const {height, width} = this.state;

        var that = this;
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
                    .attr("height", h);

        //Load in GeoJSON data
        d3.json("https://api.jsonbin.io/b/5e34b7df3d75894195e28685").then(function(json) {

            //Bind data and create one path per GeoJSON feature
            svg.selectAll("path")
                .data(json.features)
                .enter()
                .append("path")
                .attr("d", path)
                .style("fill", function(d){
                    if (d.properties.NAME === "Los Angeles" || d.properties.NAME === "Santa Barbara" ||  d.properties.NAME === "Orange" || d.properties.NAME === "Ventura" || d.properties.NAME === "Imperial" || d.properties.NAME === "San Diego"  || d.properties.NAME === "San Bernardino" || d.properties.NAME === "Riverside"){
                        return "#2a9d8f"
                    }
                })   
                .on("click", function(d){
                    if (d.properties.NAME === "Los Angeles" || d.properties.NAME === "Santa Barbara" || d.properties.NAME === "Orange" || d.properties.NAME === "Ventura" || d.properties.NAME === "Imperial" || d.properties.NAME === "San Diego" || d.properties.NAME === "San Bernardino" || d.properties.NAME === "Riverside"){
                        d3.select("#county")
                            .text(d.properties.NAME);
                        d3.select("#tooltip")
                            .classed("hidden", false);
                        d3.select(this).style("fill", "#e9c46a");
                        d3.select(that.state.prevCountyObj).style("fill", "#2a9d8f");
                        that.countyCalled(d.properties.NAME);
                        that.setState({prevCountyObj: this});

                    }
                }) 
                
        });
            
		
	}


    render() {
        return( 
        <div>
            <div className = "ca-map" ref="canvas"></div>
            <h2 id="county"></h2>
            {this.state.county !== null && this.state.prevCounty !== this.state.county ? <CountyInfo county = {this.state.county}/> : null}
        </div>)
    }
}
export default USMap