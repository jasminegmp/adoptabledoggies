import React from 'react';
import Landing from '../Landing/index';
import Loader from '../Loader/index';
import GetBreedData from '../GetBreedData/index';
import axios from 'axios';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

class App extends React.Component {

  constructor(props) {
    super(props);
    
    this.state = {
      loading: true,
      zipcodedata: null
    };
  }

  componentDidMount() {
    var self = this;
      axios.post('http://127.0.0.1:5000/counties')
          .then(function(data){
              //console.log(response);
              self.setState({zipcodedata: data});
              self.setState({loading: false});
      //Perform action based on response
      })
      .catch(function(error){
          console.log(error);
      //Perform action based on error
      });
  }
  render() {
    if(this.state.loading) {
      return <Loader/>;
    } 
    return (

      <Router>
      <Switch>
          <Route exact path='/' render={() => <Landing/>}/>
          {/*<Route exact path='/query' component={GetBreedData}/>*/}
      </Switch>
      </Router>
    );
  }
}

export default App;
