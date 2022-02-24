import React from "react";
import axios from 'axios';
import Navbar from "./components/Navbar/NavBar";


class DashBoard extends React.PureComponent {

    state = {
        isUserAuth: false
    }

    isUserAuthCallback = (auth) => {
        this.setState({
            isUserAuth: auth
        });
    }

    render() {
        return (
            <>
                <Navbar authCheck={this.state.isUserAuth}/>
            </>
        );
    }
}
export default DashBoard;