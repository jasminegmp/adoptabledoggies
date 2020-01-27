import React from 'react';
import Loader from '../Loader/index';

class CountyInfo extends React.Component {

  constructor(props) {
    super(props);
    
    this.state = {
      county: this.props.county
    };
  }

  render() {
    return (<div>Hello! {this.state.county}</div>)
    /*if(this.state.loading) {
      return <Loader/>;
    } 
    return (
        
    );*/
  }
}

export default CountyInfo;
