import React from 'react';
import { BrowserRouter as Router, Route} from 'react-router-dom'
import { ProjectCosts } from './ProjectCosts/ProjectCosts'


const App = () => (
    <Router>
        <div>
            <Route exact path='/' component={ProjectCosts} />
        </div>
    </Router>
)

export default App
