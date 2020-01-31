import React from 'react';
import LoadMap from '../LoadMap/index';
import Info from '../Info/index';
import {withRouter} from 'react-router-dom';
import './styles.scss'

class Landing extends React.Component {
  

  render() {
    return (
        <div className = "row">
          <div className = "info-background column info small-column">
            <Info/>
          </div>
          <div className = "map-background column large-column">
            <LoadMap/>
            </div>
        </div>
    );
  }
}

export default withRouter(Landing);
