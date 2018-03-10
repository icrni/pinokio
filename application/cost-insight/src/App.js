import React from 'react';
import { BrowserRouter as Router, Route} from 'react-router-dom'
import { ProjectCosts } from './ProjectCosts/ProjectCosts'
import { App as Worklogs } from './WorklogCosts/app'


const App = () => (
    <Router>
        <div>
            <Route exact path='/' component={ProjectCosts} />
            <Route strict exact path='/worklogs/' component={Worklogs} />
        </div>
    </Router>
)

export default App
