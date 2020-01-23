import React from 'react';
import * as d3 from 'd3';
import axios from 'axios';

class LoadMap extends React.Component {
    constructor(props) {
        super(props);
        
        this.state = {
            zipcodedata: this.props.zipcodedata,
            loading: true,
            height: 600,
            width: 760,
            data:null
        };
      }


    componentDidMount() {

        //this.drawMap(this.state.data);
    }

// http://bl.ocks.org/threestory/ed0f322d7bb2e3be8ded
    drawMap()  {
        const {width, height} = this.state;
        const h = height;
        const w = width; 
        // create svg
        const svgCanvas = d3.select(this.refs.canvas)
            .append("svg")
            .attr("width", w)
            .attr("height", h)
            .style("border", "1px solid black");

        //Define map projection
        var projection = d3.geoMercator()
            .center([ -120, 37 ])
            .translate([ w/2, h/2 ])
            .scale([ w*3.3 ]);

        //Define path generator
		var path = d3.geoPath()
            .projection(projection);

        
        //Load in GeoJSON data
        // from https://github.com/OpenDataDE/State-zip-code-GeoJSON/blob/master/ca_california_zip_codes_geo.min.json
        d3.json("../../storage/ca_california_zip_codes_geo.min.json", function(json) {
            console.log(json);
            //Bind data and create one path per GeoJSON feature
            svgCanvas.selectAll("path")
                .data(json.features)
                .enter()
                .append("path")
                .attr("d", path)
                .on("mouseover", function(d){
                    var xPosition = w/2 + 150;
                    var yPosition = h/2;
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

  render(){
    //console.log(this.state.results)
    return (
      <div ref="canvas"></div>
    )
  }
}
      
  export default LoadMap;