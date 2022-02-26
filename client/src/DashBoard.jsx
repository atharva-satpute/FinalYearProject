import React from "react";
import axios from 'axios';
import { Box, Button, InputBase } from '@mui/material';
import Navbar from "./components/Navbar/NavBar";

import './DashBoard.css';


class DashBoard extends React.PureComponent {

    state = {
        isUserAuth: false,
        searchID: null,
        selectedFile: null
    }

    isUserAuthCallback = (auth) => {
        this.setState({
            isUserAuth: auth
        });
    }

    onFileChange = (event) => {
        this.setState({
            selectedFile: (event) ? (event.target.files[0]) : null
        });
    }

    render() {
        return (
            <div className="dashboard-container">
                <Navbar authCheck={this.state.isUserAuth}/>
                <div className="search-container">
                    <div className="search-bar">
                        <Box
                            borderRadius={2}
                            display='flex'
                            sx={{ 
                                flexGrow: 1,
                                boxShadow: 2
                            }}
                        >
                            <InputBase
                                autoFocus
                                fullWidth
                                type="text"
                                placeholder="Search Bug ID"
                                sx={{ 
                                    flexGrow: 1, 
                                    borderRadius: 2,
                                    paddingLeft: 2
                                }}

                                onChange={(event) => {
                                    this.setState({
                                        searchID: event.target.value
                                    })
                                }}
                            />
                        </Box>
                        <Button
                            variant="contained"
                            sx={{
                                marginLeft: 1
                            }}
                        >
                            Search
                        </Button>
                    </div>
                    <p>or</p>
                    <input
                        accept=".json, .csv"
                        type={'file'}
                        onChange={(event) => {
                            this.onFileChange(event)
                        }}
                    />                 
                </div>
            </div>
        );
    }
}
export default DashBoard;