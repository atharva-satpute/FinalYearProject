import React, { useEffect } from "react";
import axios from 'axios';
import { Box, Button, Grid, IconButton, InputBase, List, ListItem, Paper, Typography } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Navbar from "./components/Navbar/NavBar";

import './DashBoard.css';
import { useState } from "react";
import config from "./config/config.json";
import DataTable from "./components/DataTable/DataTable";
import DropDownBox from "./components/DropDownBox/DropDownBox";



const DashBoard = () => {

    const [searchID, setSearchID] = useState("");
    const [listSearchID, setListSearchID] = useState("");
    const [selectedFile, setSelectedFile] = useState(null);
    const [receivedData, setReceivedData] = useState(null);
    const [receivedReport, setReceivedReport] = useState(null);
    const [receivedItemReport, setReceivedItemReport] = useState(null);
    const [dropDownList, setDropDownList] = useState([]);

    let buglistElement = document.getElementById('bug-list');
    let reportToDisplay = document.getElementById('report');
    let backButton = document.getElementById('back-button');

    
    const onFileChange = (event) => {
        setSelectedFile((event) ? event.target.files[0] : null);
    }

    const onDropListChange = (event) => {
        setListSearchID(event.target.value)
    }

    useEffect(() => {
        if(listSearchID !== "") {
            handleSearch(listSearchID)
        }        
    },[listSearchID])

    function handleSearch(id) {
        if(id === "")
            alert('Enter Bug Id');
        else {
        
            let URL = `http://${config.server.url}:${config.server.port}/search/${id}`;

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
    }

    const onFileUpload = () => {
        let formData = new FormData();
        formData.append(
            "file",
            selectedFile,
            selectedFile.name
        );
        if(selectedFile){
            // POST data to server
            axios.post(
                `http://${config.server.url}:${config.server.port}/upload`,
                formData,
                {
                    headers:{"Content-Type" : "multipart/form-data"}
                }
            )
            .then((response) => {
                console.log("Response:",response);
                setDropDownList(response.data);
            })
            .catch((error) => {
                console.log("Error:",error.response.data);
            })
        }
    }

    const onBackButtonClick = () => {
        buglistElement.style.display = 'block';
        reportToDisplay.style.display = 'none';
        backButton.style.display = 'none';
    }

    function itemClicked(listItemID) {
        buglistElement.style.display = 'none';
        reportToDisplay.style.display = 'block';
        backButton.style.display = 'block';

        let URL = `http://${config.server.url}:${config.server.port}/search/${listItemID}`;
        axios.get(
            URL
        )
        .then((response) => {
            setReceivedItemReport(response.data)
        })
        .catch((error) => {
            console.log('Error in receiving onClick report',error.response.data);
        })
    }

    return (
        <div className="dashboard-container">
            <Navbar />
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
                            maxWidth: '100%',
                            maxHeight: '100%',
                            marginLeft: 1
                        }}
                        onClick={() => {
                            handleSearch(searchID)
                        }}
                    >
                        Search
                    </Button>
                </div>
                <span>or</span>
                <div className="file-upload-section">
                    <input
                        accept=".json, .csv"
                        type={'file'}
                        onChange={(event) => {
                            onFileChange(event)
                        }}
                    />
                    <Button
                        variant="contained"
                        sx={{ height: '25px' }}
                        onClick={ onFileUpload }
                    >
                        Upload
                    </Button>
                </div>                
            </div>
            <div className="output-container">
                <div id="back-button">
                    <IconButton onClick={onBackButtonClick}>
                        <ArrowBackIcon />
                    </IconButton>
                </div>
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
                        <div className="select-dropbox">
                            <DropDownBox
                                bugList={dropDownList}
                                onSelect={onDropListChange}
                            />
                        </div>
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
                        <div id="change-output">
                            <div id="bug-list">
                                {
                                    (receivedData) ?
                                    (
                                        <List>
                                            {
                                                receivedData.map((data) => {
                                                    let key = Object.keys(data);
                                                    return(
                                                        <ListItem 
                                                            id={ key[0] }
                                                            key={ key[0] }
                                                            sx={{ cursor: "pointer" }}
                                                            onClick={() => {
                                                                itemClicked(key[0])
                                                            }}
                                                        >
                                                            <Paper sx={{ width:'100%', paddingLeft:1}} >
                                                                <Typography >
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
                            </div>
                            <div id="report">
                                {
                                    (receivedItemReport) ?
                                    <DataTable content={receivedItemReport} />
                                    :
                                    <h1>No report found</h1>
                                }                                
                            </div>
                        </div>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}
export default DashBoard;