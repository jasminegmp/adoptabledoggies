import React from 'react';
import * as d3 from 'd3';

class BreedVisualization extends React.Component {
    constructor(props) {
        super(props);
        
        this.state = {
            loading: true,
            results: this.props.data.data, 
            height: 700,
            width: 1000,
            margin: {top: 20, right: 20, bottom: 30, left: 40}
        };
      }

    componentDidMount() {
        //this.drawChart();
        this.drawBarChart(this.state.results.slice(0,5));// just get the top 5 dog breeds,
    }
   
    drawChart = () => {
      const {width, height, data} = this.state;
      let margin = {top: 20, right: 20, bottom: 30, left: 40};
      /*
      const svg = d3.select("body")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .style("margin-left", 100);
                      */

      // set the ranges
      let x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);
      let y = d3.scaleLinear()
        .range([height, 0]);
      
      // append the svg object to the body of the page
      // append a 'group' element to 'svg'
      // moves the 'group' element to the top left margin
      var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");
      
      data.forEach(function(d) {
        
        d.breed_name = d[1];
        d.breed_count += d[2];
        
        // Scale the range of the data in the domains
        x.domain(data.map(function(d) { return d.breed_name; }));
        y.domain([0, d3.max(data, function(d) { return d.breed_name; })]);

        console.log(data);
        // append the rectangles for the bar chart
        svg.selectAll("bar")
            .data(data)
          .enter().append("rect")
            .attr("fill", "steelblue")
            .attr("x", function(d) { return x(d.breed_name); })
            .attr("width", x.bandwidth())
            .attr("y", function(d) { return y(d.breed_count); })
            .attr("height", function(d) { return height - y(d.breed_count); });

      });

      // add the x Axis
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));
  
      // add the y Axis
      svg.append("g")
            .call(d3.axisLeft(y));



/*
        svg.selectAll("rect")
            .data(data[2])
            .enter()
            .append("rect")
            .attr("x", (d, i) => i * 70)
            .attr("y", (d, i) => h - 10 * d)
            .attr("width", 65)
            .attr("height", (d, i) => d * 10)
            .attr("fill", "green")

        svg.selectAll("text")
            .data(data[1])
            .enter()
            .append("text")
            .text((d) => d)
            .attr("x", (d, i) => i * 70)
            .attr("y", (d, i) => h - (10 * d) - 3)*/
    }


    drawBarChart(data)  {
      const {margin, width, height} = this.state;


      const svgCanvas = d3.select(this.refs.canvas)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("border", "1px solid black")
    
      console.log(data);

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