import React from 'react';
import * as d3 from 'd3';
import './styles.scss';

class D3CountyViz extends React.Component {

  constructor(props) {
    super(props);
    
    this.state = {
      results: this.props.data,
      height: 250,
      width: 250,
      margin: {top: 5, right: 5, bottom: 5, left: 5}
    };
  }

    componentDidMount() {

        const {results, margin, width, height} = this.state;

        // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
        let radius = Math.min(width, height) / 2 * 0.8;

        const svgCanvas = d3.select(this.refs.canvas)
            .append("svg")
            .attr('viewBox','0 0 '+Math.min(width,height) +' '+Math.min(width,height) )
            .style("border", "1px solid black")
            .attr("width", width)
            .attr("height", height)
        
        const g = svgCanvas.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
        var color = d3.scaleOrdinal(['#e76f51','#2a9d8f']);
    
        //console.log(results.gender)
        // Generate the pie
        var pie = d3.pie();

        // Generate the arcs
        var arc = d3.arc()
                    .innerRadius(0)
                    .outerRadius(radius);

        // Create array of objects of search results to be used by D3
        var data = [];
        Object.entries(results.gender).forEach(([key, value]) => {
            console.log(key, value)
            data.push({
                count: value,
                name: key
              });
 
        })


        console.log(data)
        //Generate groups
        var arcs = g.selectAll("arc")
                    .data(pie(data.map(d => d.count)))
                    .enter()
                    .append("g")
                    .attr("class", "arc")
                    

        //Draw arc paths
        arcs.append("path")
            .attr("fill", function(d, i) {
                return color(i);
            })
            .attr("d", arc);

        arcs.selectAll("path")
            .transition()
                .delay(function(d, i) {
                return i * 800;
                })
                    .attrTween('d', function(d) {
            var i = d3.interpolate(d.startAngle+0.1, d.endAngle);
            return function(t) {
                d.endAngle = i(t);
                return arc(d);
            }
            });
            

        const arcLabel =  d3.arc().innerRadius(radius).outerRadius(radius);
            
       /* arcs.append("text")
            .attr("transform", function(d) { 
                    return "translate(" + arcLabel.centroid(d) + ")"; 
            })
            .text(data.map(d => d.count));*/

        // again rebind for legend
        
        var legendG = svgCanvas.selectAll(".legend") // note appending it to mySvg and not svg to make positioning easier
        .data(pie(data))
        .enter().append("g")
        .attr("transform", function(d,i){
            return "translate(" + 0 + "," + (i * 15 + 10) + ")"; // place each legend on the right and bump each one down 15 pixels
        })
        .attr("class", "legend");   

        legendG.append("rect") // make a matching color rect
        .attr("width", 10)
        .attr("height", 10)
        .attr("fill", function(d, i) {
            return color(i);
        });

        legendG.append("text") // add the text
        .text(function(d){
            return d.data.name + "  " + d.data.count;
        })
        .style("font-size", 12)
        .attr("y", 10)
        .attr("x", 11);

    }


    


    render() {
        return (
            <div ref="canvas"></div>
        );
    }
}

export default D3CountyViz;
