import React from 'react';
import Landing from '../Landing/index';
import Loader from '../Loader/index';
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
      axios.get('https://api.jsonbin.io/b/5e34b7df3d75894195e28685')
          .then(function(data){
              self.setState({zipcodedata: data});
              self.setState({loading: false});
      })
      .catch(function(error){
          console.log(error);
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
      </Switch>
      </Router>
    );
  }
}

export default App;
