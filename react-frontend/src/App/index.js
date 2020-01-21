import React from 'react';
import Landing from '../Landing/index';
import GetBreedData from '../GetBreedData/index';

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

class App extends React.Component {
  
  render() {
    return (

      <Router>
      <Switch>
          <Route exact path='/' component={Landing}/>
          <Route exact path='/query' component={GetBreedData}/>
      </Switch>
      </Router>
    );
  }
}

export default App;
