import React from 'react';
import * as d3 from 'd3';

class BreedVisualization extends React.Component {
    constructor(props) {
        super(props);
        
        this.state = {
            result: null,
            loading: true,
            results: this.props.data.data.data.slice(0,5), // just get the top 5 dog breeds,
            id: "root",
            height: 700,
            width: 500
        };
      }

    componentDidMount() {
        this.drawChart();
    }
   
    drawChart = () => {
        const data = [1,2,3,4,5];
        
        const svg = d3.select("body")
        .append("svg")
        .attr("width", this.state.width)
        .attr("height", this.state.height)
        .style("margin-left", 100);
                        
        const h = this.state.height;

        svg.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", (d, i) => i * 70)
            .attr("y", (d, i) => h - 10 * d)
            .attr("width", 65)
            .attr("height", (d, i) => d * 10)
            .attr("fill", "green")

        svg.selectAll("text")
            .data(data)
            .enter()
            .append("text")
            .text((d) => d)
            .attr("x", (d, i) => i * 70)
            .attr("y", (d, i) => h - (10 * d) - 3)
    }

  render(){
    console.log(this.state.results)
    return (<div>hi and
    <div id={"#" + this.state.id}></div></div>)
  }
}
      
  export default BreedVisualization;