import React from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import USMap from './WorldMap.js';


class LoadMap extends React.Component {
  
    constructor(props) {
      super(props);
      
      this.state = {
        loading: this.props.loading
      };
    }
  
  
    render() {
      return (
          <div>
              hi
              <USMap/>
          </div>
      );
    }
  }
   
  export default LoadMap;