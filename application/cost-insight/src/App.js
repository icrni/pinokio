import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './App.css';

import _ from 'lodash'
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar'
import {CostTable} from './Costs'

import ReactTable from "react-table";
import "react-table/react-table.css";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      labels: []
    }
  }

  loadData() {
    fetch('http://127.0.0.1:8000/roadmap/costs/')
      .then(response => response.json())
      .then(data => this.setState({ labels: data}));
  }

  componentDidMount() {
    this.loadData();
    //window.setInterval(this.loadData.bind(this), 60000);
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
      <div>
      <ReactTable
        data={this.state.labels}
        columns={[
          {
            Header: "Label",
            accessor: "label"
          },
          {
            Header: "Year",
            accessor: "year"
          },
          {
            Header: "Week",
            accessor: "week"
          },
          {
            Header: "PID",
            accessor: "PID"
          },
          {
            Header: "Cost (EUR)",
            accessor: "cost",
            aggregate: vals => _.sum(vals),
            filterable: false
          }
        ]}
      className="-striped -highlight"
      pivotBy={["label", "year", "week", "PID"]}
      filterable
      />
      </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
 