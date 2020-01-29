import React from 'react';
import LoadMap from '../LoadMap/index';
import Info from '../Info/index';
import {withRouter} from 'react-router-dom';
import './styles.scss'

class Landing extends React.Component {
  

  render() {
    return (
        <div class = "row">
          <div class = "info-background column info small-column">
            <Info/>
          </div>
          <div class = "column large-column">
            <LoadMap/>
            </div>
        </div>
    );
  }
}

export default withRouter(Landing);
