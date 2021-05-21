import React from 'react';
import { render } from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Home from './Home';
import Main from './Main';

const App = () => (
  <Router>
    <Route exact path="/" component={Home} />
    <Route path="/classifier" component={Main} />
  </Router>
);

export default App;