import React from 'react';
import './App.css';
import Nav from './components/nav';
import About from './components/about';
import Shop from './components/shop';
import ItemDetail from './components/detail';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Nav />
          <Switch>
            <Route path="/about" exact component={About} />
            <Route path="/shop" exact component={Shop} />  
            <Route path='/shop/:id' exact component={ItemDetail} />
          </Switch>
      </div>
    </Router>
  );
}

export default App;
