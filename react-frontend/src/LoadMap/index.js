import React from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import USMap from './WorldMap.js';


class LoadMap extends React.Component {
  
    constructor(props) {
      super(props);
      
      this.state = {
        loading: this.props.loading,
        zipcodedata: this.props.zipcodedata
      };
    }
  
  
    render() {
      return (
          <div>
              hi
              <USMap counties={this.state.zipcodedata}/>
          </div>
      );
    }
  }
   
  export default LoadMap;