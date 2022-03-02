import React from "react";
import axios from 'axios';
import { Box, Button, InputBase } from '@mui/material';
import Navbar from "./components/Navbar/NavBar";

import './DashBoard.css';
import { useNavigate } from "react-router-dom";
import { useState } from "react";


const DashBoard = () => {

    const [isUserAuth, setUserAuth] = useState(false);
    const [searchID, setSearchID] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);

    const isUserAuthCallback = (auth) => {
        setUserAuth(auth);
    }

    const onFileChange = (event) => {
        setSelectedFile((event) ? event.target.files[0] : null);
    }

    return (
        <div className="dashboard-container">
            <Navbar authCheck={isUserAuth}/>
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
                                setSearchID(event.target.value);
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
                        onFileChange(event)
                    }}
                />                 
            </div>
        </div>
    );
}
export default DashBoard;