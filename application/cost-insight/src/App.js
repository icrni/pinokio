import moment from 'moment'
import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './App.css';

import RaisedButton from 'material-ui/RaisedButton';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar'


class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      labels: []
    }
  }

  loadData() {
    fetch('http://127.0.0.1:8000/roadmap/labels/')
      .then(response => response.json())
      .then(data => this.setState({ labels: data}));
  }

  componentDidMount() {
    this.loadData();
    window.setInterval(this.loadData.bind(this), 60000);
  }

  render() {
    return (
      <MuiThemeProvider>
      <div className="App">
        <Toolbar>
          <ToolbarGroup>
            <ToolbarTitle text="Cost Insights" />
          </ToolbarGroup>
        </Toolbar>
      </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
 