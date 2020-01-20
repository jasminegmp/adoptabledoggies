import React from 'react';
import Landing from '../Landing/index';
import DataViz from '../DataViz/index';

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

class App extends React.Component {
  
  render() {
    return (

      <Router>
      <Switch>
          <Route exact path='/' component={Landing}/>
          <Route exact path='/query' component={DataViz}/>
      </Switch>
      </Router>
    );
  }
}

export default App;
