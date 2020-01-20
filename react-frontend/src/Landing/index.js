import React from 'react';
import "../Button/styles.scss";
//import BarChart from '../BarChart/index';

import {Link, withRouter} from 'react-router-dom';

class Landing extends React.Component {
  
  constructor(props) {
    super(props);
    
    this.state = {
        run: false,
        data: null,
        width: 700,
        height: 500,
        id: "root",
        submit: false
    };
  }
/*
  componentDidMount() {

    var self = this;
      axios.post('http://127.0.0.1:5000/')
          .then(function(data){
              //console.log(response);
              self.setState({data: data});
              self.setState({loading: false});
      //Perform action based on response
      })
      .catch(function(error){
          console.log(error);
      //Perform action based on error
      });
  }*/

  handleSubmit = async (event) =>{
    event.preventDefault();
    this.setState({submit: true})
    
}
    

  render() {
    return (
        <div>
            <button><Link to='/query'>Get data</Link></button>
        </div>
    );
  }
}

export default withRouter(Landing);
