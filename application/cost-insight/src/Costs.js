import React, { Component } from 'react';
import {map} from 'lodash'
import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn,
  } from 'material-ui/Table';


class CostTable extends Component {
    state = {
        stripedRows: true,
        showRowHover: true,
        selectable: false,
        showCheckboxes: false
      };

    render() {
        return (
            <div class="content">
            <h2>{this.props.label}</h2>
            
            <Table showCheckboxes={this.state.showCheckboxes} >
                <TableHeader
                    displaySelectAll={this.state.showCheckboxes}
                    adjustForCheckbox={this.state.showCheckboxes }>
                <TableRow>
                    <TableHeaderColumn>Week</TableHeaderColumn>
                    <TableHeaderColumn>Cost</TableHeaderColumn>
                </TableRow>
                </TableHeader>
                <TableBody>
                    {map(this.props.data, (data, key) => <CostRow week={key} cost={data} />)}
                </TableBody>
            </Table>
            </div>
        );
    }
}

class CostRow extends Component {
    render() {
        return (
            <TableRow>
                <TableRowColumn>{this.props.week}</TableRowColumn>
                <TableRowColumn>{this.props.cost}</TableRowColumn>
            </TableRow>
        )
    }
}

export {CostTable}
