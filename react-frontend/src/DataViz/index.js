import React from 'react';
import * as d3 from 'd3';
import axios from 'axios';

class DataViz extends React.Component {

    constructor(props) {
        super(props);
        
        this.state = {
            loading: true,
            data: null,
            width: 700,
            height: 500,
            id: "root",
            submit: false
        };
    }
    
  componentDidMount() {

    var self = this;
    axios.post('http://127.0.0.1:5000/query')
        .then(function(response){
            //console.log(response);
            self.setState({data: response});
            self.setState({loading: false});
    //Perform action based on response
    })
    .catch(function(error){
        console.log(error);
    //Perform action based on error
    });
    //this.drawChart(this.state.data);
  }

    
  drawChart = (response) => {
      const data = response;
      
      const svg = d3.select("body")
      .append("svg")
      .attr("width", this.props.width)
      .attr("height", this.props.height)
      .style("margin-left", 100);
                      
      const h = this.props.height;

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

  renderItem = (dog, index) =>{
      console.log(dog)
        return(
            <div>
                <h1>{dog[1]} :{dog[2]}</h1>
            </div>
        )
}
        
  render(){
    return ( <div>
        {this.state.loading ? null : 
        this.state.data.data.data.map((dog, index) => this.renderItem(dog, index))
        }
        </div>
    )
  }
  }
      
  export default DataViz;