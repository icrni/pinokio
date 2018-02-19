import React, { Component } from 'react';
import ActionAlarm from 'material-ui/svg-icons/action/alarm';
import ContentNextWeek from 'material-ui/svg-icons/content/next-week';
import moment from 'moment'

const iconStyles = {
    "height": 15,
    "padding-top": 2
};


class DateLabel extends Component {
    render() {
        return (
            <p>{this.props.text}</p>
        );
    }
}

class WorkerLabel extends Component {
    render() {
        return (
            <p className="WorkerLabel">{this.props.text}</p>
        );
    }
}

class Issue extends Component {
    render() {
        switch(this.props.data.status) {
            case 'To Do':
                var color = 'grey';
                break;
            case 'In progress':
                var color = 'khaki';
                break;
            case 'Code review':
                var color = '#D6BF86';
                break;
            case 'Ready to ship':
                var color = '#A6AF7A';
                break;
            case 'Done':
                var color = '#669966';
                break;
            case 'Ready':
                var color = 'steelblue';
                break;
            default:
                var color = 'grey';
                break;
        }
        var issueStyle = {
            "width": this.props.width + '%',
            "background-color": color
        };

        return(
            <div className="Issue" style={issueStyle}>
            {this.props.data.key}- {this.props.data.status}<br/>
            <ActionAlarm style={iconStyles}/> {this.props.data.logged} h <ContentNextWeek style={iconStyles}/> {this.props.data.commits}

            </div>
        );
    }
}

class DayColumn extends Component {
    render() {
        if (this.props.data && this.props.data.length != 0)  {
            var width = 95 / this.props.data.length; 
        } else {
            return (<div className="WeekDay"></div>);
        }
        
        return (
            <div className="WeekDay">
                {this.props.data.map((data) => <Issue data={data} width={width} />)}
            </div>
        );
    }
}

class RoadmapRow extends Component {
    render() {
        const start_date = moment.unix(this.props.start_date);
        var columns = [];
        for(var i=0; i < 5; i++) {
            let date = moment.unix(this.props.start_date).add(i, "days").format("DD.MM.YYYY");
            columns.push(<DayColumn data={this.props.data[date]} />)
        }
        return(columns);
    }
}

export { DateLabel, WorkerLabel, RoadmapRow };
