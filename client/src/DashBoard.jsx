import React from "react";
import axios from 'axios';
import { Box, Button, Grid, InputBase, List, ListItem, Paper, Typography } from '@mui/material';
import Navbar from "./components/Navbar/NavBar";

import './DashBoard.css';
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import config from "./config/config.json";
import DataTable from "./components/DataTable/DataTable";




const DashBoard = () => {

    const [isUserAuth, setUserAuth] = useState(false);
    const [searchID, setSearchID] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [receivedData, setReceivedData] = useState(null);
    const [receivedReport, setReceivedReport] = useState(null);

    const isUserAuthCallback = (auth) => {
        setUserAuth(auth);
    }

    const onFileChange = (event) => {
        setSelectedFile((event) ? event.target.files[0] : null);
    }

    function handleSearch() {
        let URL = `http://${config.server.url}:${config.server.port}` + `/search/${searchID}`;

        // Fetch the report with ID=searchID
        axios.get(
            URL
        )
        .then((response) => {
            setReceivedReport(response.data)
        })
        .catch((error) => {
            console.log('Error in receiving the report',error.response.data);
        });

        // POST the searchID
        axios.post(
            URL
        )
        .then((response) => {
            setReceivedData(response.data.result)
        })
        .catch((error) => {
            console.log('Bug Report error:',error.response.data);
        });
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
                        onClick={handleSearch}
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
            <div className="output-container">
                <Grid container columns={16}>
                    <Grid
                        item
                        xs={16} md={8}
                        sx={{
                            height:'100%', 
                            position: 'relative',
                            overflowY: 'auto',
                            maxHeight: 675
                        }}
                    >
                        {
                            (receivedReport) ?
                            <DataTable content={receivedReport}/>
                            :
                            <h1>No report</h1>
                        }
                        
                    </Grid>
                    <Grid 
                        item
                        xs={16}
                        md={8}
                        bgcolor='rgb(192,192,192)'
                        sx={{
                            position: 'relative',
                            overflowY: 'auto',
                            minHeight: 675,
                            maxHeight: 675
                        }}
                    >
                        {
                            (receivedData) ?
                            (
                                <List>
                                    {
                                        receivedData.map((data) => {
                                            let key = Object.keys(data);
                                            return(
                                                <ListItem key={ key[0] }>
                                                    <Paper sx={{ width:'100%', paddingLeft:1 }} >
                                                        <Typography>
                                                                Bug ID: { key[0] }
                                                        </Typography>
                                                        <Typography>
                                                            Score: { data[key[0]] }
                                                        </Typography>
                                                    </Paper>
                                                </ListItem>
                                            );
                                        })
                                    }                       
                                </List>
                            )
                            :
                            (
                                <h2>No similar reports</h2>
                            )
                        }
                        
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}
export default DashBoard;