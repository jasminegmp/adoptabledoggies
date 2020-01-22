import React from 'react';
import * as d3 from 'd3';

class BreedVisualization extends React.Component {
    constructor(props) {
        super(props);
        
        this.state = {
            loading: true,
            results: this.props.data.data, 
            height: 500,
            width: 500,
            margin: {top: 5, right: 5, bottom: 5, left: 5}
        };
      }

    componentDidMount() {
        //this.drawChart();
        this.drawBarChart(this.state.results.slice(0,5));// just get the top 5 dog breeds,
    }


    drawBarChart(data)  {
      const {margin, width, height} = this.state;

      // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
      let radius = Math.min(width, height) / 2 * 0.8;


      const svgCanvas = d3.select(this.refs.canvas)
        .append("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .style("border", "1px solid black");
    
      console.log(data);

      let pie = d3.pie()
        .sort(null)
        .value(d => d.count)

      let arc = d3.arc()
        .innerRadius(0)
        .outerRadius(Math.min(width, height) / 2 - 1)

      // set the color scale
      let color = d3.scaleOrdinal()
        .domain(data.map(d => d.name))
        .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse())

      const arcs = pie(data);

      const arcLabel =  d3.arc().innerRadius(radius).outerRadius(radius);

      svgCanvas.append("g")
          .attr("stroke", "white")
        .selectAll("path")
        .data(arcs)
        .join("path")
          .attr("fill", d => color(d.data.name))
          .attr("d", arc)
        .append("title")
          .text(d => `${d.data.name}: ${d.data.count.toLocaleString()}`);
  
        
      svgCanvas.append("g")
          .attr("font-family", "sans-serif")
          .attr("font-size", 12)
          .attr("text-anchor", "middle")
        .selectAll("text")
        .data(arcs)
        .join("text")
          .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
          .call(text => text.append("tspan")
              .attr("y", "-0.4em")
              .attr("font-weight", "bold")
              .text(d => d.data.name))
          .call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
              .attr("x", 0)
              .attr("y", "0.7em")
              .attr("fill-opacity", 0.7)
              .text(d => d.data.count.toLocaleString()));

      /*
      const x = d3.scaleBand()
        .domain(d3.range(data.length))
        .range([margin.left, width - margin.right])
        .padding(0.1)

      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count)]).nice()
        .range([height - margin.bottom, margin.top])

      svgCanvas.selectAll("rect")
        .data(data).enter()
            .append("rect")
            .attr("x", (d, i) => x(i))
            .attr("y", d => y(d.count))
            .attr("height", d => y(0) - y(d.count))
            .attr("width", 100);
*/
     /* svgCanvas.selectAll("text")
        .data(data[1])
        .enter()
        .append("text")
        .text((d) => d)
        .attr("x", (d, i) => i * 70)
        .attr("y", (d, i) => height - (10 * d) - 3);*/
    }

  render(){
    //console.log(this.state.results)
    return (
      <div ref="canvas"></div>
    )
  }
}
      
  export default BreedVisualization;