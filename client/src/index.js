import React from 'react';
import ReactDOM from 'react-dom';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import SignIn from './components/SignIn/SignIn';
import SignUp from './components/SignUp/SignUp';
import DashBoard from './DashBoard';

import './index.css';


ReactDOM.render(
    <Router>
        <Routes>
            <Route path='/' exact element={<DashBoard />}/>
            <Route path='/signIn' element={<SignIn />}/>
            <Route path='/signUp' element={<SignUp />}/>
        </Routes>
    </Router>,
    document.getElementById('root')
);
