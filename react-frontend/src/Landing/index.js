import React from 'react';
import "../Button/styles.scss";
import LoadMap from '../LoadMap/index';
import axios from 'axios';

import {Link, withRouter} from 'react-router-dom';

class Landing extends React.Component {
  
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
            <LoadMap zipcodedata = {this.state.zipcodedata}/>
            {/*<button><Link to='/zipcode'>Get Zipcode</Link></button>*/}
        </div>
    );
  }
}

export default withRouter(Landing);
