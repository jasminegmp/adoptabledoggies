import React from 'react';
import "../Button/styles.scss";
import LoadMap from '../LoadMap/index';
import axios from 'axios';

import {Link, withRouter} from 'react-router-dom';

class Landing extends React.Component {
  

  render() {
    return (
        <div>
            <LoadMap/>
        </div>
    );
  }
}

export default withRouter(Landing);
