import moment from 'moment'
import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import './App.css';

import RaisedButton from 'material-ui/RaisedButton';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar'
import { WorkerLabel, RoadmapRow } from './Roadmap'

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      date_from: moment().startOf('isoweek'),
      date_to: moment().endOf('isoweek'),
      issues: []
    }
  }

  loadData() {
    fetch('http://127.0.0.1:8000/roadmap/days/' + this.state.date_from.unix() + '/' + this.state.date_to.unix() + '/')
      .then(response => response.json())
      .then(data => this.setState({ issues: data}));
  }

  componentDidMount() {
    this.loadData();
  }

  handlePreviousWeek() {
    this.setState({ date_from: this.state.date_from.subtract(1, 'weeks').startOf('isoweek'), date_to: this.state.date_to.subtract(1, 'weeks').endOf('isoweek') })
    this.loadData();
  }

  handleNextWeek() {
    this.setState({ date_from: this.state.date_from.add(1, 'weeks').startOf('isoweek'), date_to: this.state.date_to.add(1, 'weeks').endOf('isoweek') })
    this.loadData();
  }

  render() {
    const period = this.state.date_from.format("DD.MM.YYYY") + ' - ' + this.state.date_to.format("DD.MM.YYYY")
    const start_date = this.state.date_from.unix();
    return (
      <MuiThemeProvider>
      <div className="App">
        <Toolbar>
          <ToolbarGroup>
            <ToolbarTitle text="Development plan" />
            <RaisedButton label="Previous week" onClick={() => this.handlePreviousWeek()}/>
            <ToolbarTitle text={period} />
            <RaisedButton label="Next week" onClick={() => this.handleNextWeek()}/>
          </ToolbarGroup>
        </Toolbar>
        <div className="RoadmapRow">
          <div className="WorkerColumnLabel"></div>
          <div className="WeekDayLabel">Monday</div>
          <div className="WeekDayLabel">Tuesday</div>
          <div className="WeekDayLabel">Wednesday</div>
          <div className="WeekDayLabel">Thursday</div>
          <div className="WeekDayLabel">Friday</div>
        </div>
        { Object.keys(this.state.issues).map((worker) => {
          return (<div  className="RoadmapRow">
            <div className="WorkerColumn"><WorkerLabel text={worker} /></div>
            <RoadmapRow data={this.state.issues[worker]} start_date={start_date} />
          </div>);
        })}
      </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
 