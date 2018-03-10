import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './app.css';

import _ from 'lodash'
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar'
import ReactTable from "react-table";
import "react-table/react-table.css";
import moment from 'moment'
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import AmCharts from 'amcharts3'


class App extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        date_from: moment().startOf('isoweek'),
        date_to: moment().endOf('isoweek'),
        worklogs: []
      }
      this.setDateFrom = this.setDateFrom.bind(this);
      this.setDateTo = this.setDateTo.bind(this);
    }
  
    loadData() {
      fetch('http://127.0.0.1:8000/roadmap/weekcosts/' + this.state.date_from.unix() + '/' + this.state.date_to.unix() + '/')
        .then(response => response.json())
        .then(data => this.setState({ worklogs: data}));
    }

    setDateFrom(date) {
        this.setState({
          date_from: date
        }, () => {
            this.loadData();
        });
    }

    setDateTo(date) {
        this.setState({
            date_to: date
          }, () => {
              this.loadData();
          });
    }

    componentDidMount() {
        this.loadData();
      }

    render() {
        return (
            <MuiThemeProvider>
            <div className="App">
              <Toolbar>
                <ToolbarGroup>
                  <ToolbarTitle text="Cost Insights" />
                    <DatePicker
                        selected={this.state.date_from}
                        onChange={this.setDateFrom}
                    />
                    <DatePicker
                        selected={this.state.date_to}
                        onChange={this.setDateTo}
                    />
                </ToolbarGroup>
              </Toolbar>
            </div>
            <div>
            <ReactTable
              data={this.state.worklogs}
              columns={[
                {
                    Header: "PID",
                    accessor: "PID",
                    width: 600
                },
                {
                    Header: "Issue",
                    accessor: "issue"
                },
                {
                    Header: "Worker",
                    accessor: "worker"
                },
                {
                    Header: "Day",
                    accessor: "day"
                },
                {
                  Header: "Hours",
                  accessor: "total",
                  width: 150,
                  aggregate: vals => _.sum(vals),
                  filterable: false,
                  Cell: row => <span className='table_values'>{row.value} h</span>,
                  Footer: <span className='foot_table_values'>{_.sum(_.map(this.state.worklogs, d => d.total))} h</span>
                },
                {
                  Header: "Cost",
                  accessor: "cost",
                  width: 150,
                  aggregate: vals => _.sum(vals),
                  filterable: false,
                  Cell: row => <span className='table_values'>{row.value} EUR</span>,
                  Footer: <span className='foot_table_values'>{_.sum(_.map(this.state.worklogs, d => d.cost))} EUR</span>
                }
              ]}
            className="-striped -highlight"
            pivotBy={["PID", "issue"]}
            />
            </div>
            
            </MuiThemeProvider>
          );
    }
}

export {App}
