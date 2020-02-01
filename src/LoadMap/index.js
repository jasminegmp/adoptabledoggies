import React from 'react';
import USMap from './USMap.js';


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
            <h3>Click on a Southern California County</h3>
              <USMap/>
          </div>
      );
    }
  }
   
  export default LoadMap;