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
import LoadingSpinner from "./components/LoadingSpinner/LoadingSpinner";



const DashBoard = () => {

    const regexExp = /[a-zA-Z0-9]/;
    const charNotRequired = /[^a-zA-Z0-9,]/;

    const [searchID, setSearchID] = useState("");
    const [listSearchID, setListSearchID] = useState("");
    const [selectedFile, setSelectedFile] = useState(null);
    const [receivedData, setReceivedData] = useState([]);
    const [receivedReport, setReceivedReport] = useState(null);
    const [receivedItemReport, setReceivedItemReport] = useState(null);
    const [dropDownList, setDropDownList] = useState([]);
    const [isLoadingReport,setIsLoadingReport] = useState(false);
    const [isLoadingList, setIsLoadingList] = useState(false);

    let buglistElement = document.getElementById('bug-list');
    let reportToDisplay = document.getElementById('report');
    let backButton = document.getElementById('back-button');

    
    const onFileChange = (event) => {
        setSelectedFile((event) ? event.target.files[0] : null);
    }

    const onDropListChange = (event) => {
        setListSearchID(event.target.value)
    }

    const onClickSearchButton = () => {
        if(searchID.trim().length === 0){
            alert('Enter Bug ID');
            return;
        }

        setIsLoadingList(true);
        setIsLoadingReport(true);
        let list = searchID.split(',');
        if(list.length > 1){
            setDropDownList(list);
            setListSearchID(list[0]);
        }
        else {
            setDropDownList([]);
            handleSearch(list[0]);
        }
    }

    useEffect(() => {
        if(listSearchID !== "") {
            handleSearch(listSearchID)
        }        
    },[listSearchID])

    function handleSearch(id) {
        let URL = `http://${config.server.url}:${config.server.port}/search/${id}`;

        // Fetch the report with ID=searchID
        axios.get(
            URL
        )
        .then((response) => {
            setReceivedReport(response.data);
            setIsLoadingReport(false);
        })
        .catch((error) => {
            console.log('Error in receiving the report',error.response.data);
        });

        // POST the searchID
        axios.post(
            URL
        )
        .then((response) => {
            if(Object.keys(response.data).length > 0)
                setReceivedData(response.data.result);
            else
                setReceivedData([]);
            setIsLoadingList(false);
        })
        .catch((error) => {
            console.log('Bug Report error:',error.response.data);
            setIsLoadingList(false);
        });
    }

    const onFileUpload = () => {
        if(selectedFile == null){
            alert("Please upload file");
            return;
        }
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
            <div className="nav-bar">
                <Navbar />
            </div>
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

                            onKeyDown={(event) => {
                                let list = event.target.value.split(',');

                                // Search results when Enter is pressed
                                if(event.key === 'Enter')
                                    onClickSearchButton();

                                else if(event.key === 'Backspace')
                                    return true;
                                
                                // Show alert box when user tries to enter more than 3 IDs
                                else if(list.length > 3 && regexExp.test(event.key)){
                                    alert('Max 3 comma-separated IDs. For more than 3 IDs, upload a .csv file');
                                    event.preventDefault();
                                    event.stopPropagation();
                                }

                                // To exclude special characters
                                else if(charNotRequired.test(event.key)){
                                    event.preventDefault();
                                    event.stopPropagation();
                                }
                            }}

                            onChange={(event) => {
                                setSearchID(event.target.value);
                            }}
                        />
                    </Box>
                    <Button
                        variant="contained"
                        disabled={isLoadingList && isLoadingReport}
                        sx={{
                            maxWidth: '100%',
                            maxHeight: '100%',
                            marginLeft: 1
                        }}
                        onClick={onClickSearchButton}
                    >
                        Search
                    </Button>
                </div>
                <span>or</span>
                <div className="file-upload-section">
                    <input
                        accept=".csv"
                        type={'file'}
                        title={'Upload file containing bug ids'}
                        onChange={(event) => {
                            onFileChange(event)
                        }}
                    />
                    <Button
                        variant="contained"
                        disabled={isLoadingList && isLoadingReport}
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
                            height: 582, 
                            position: 'relative',
                            overflowY: 'auto',
                            minHeight: 582,
                            maxHeight: 675
                        }}
                    >
                        <div className="select-dropbox">
                            <DropDownBox
                                bugList={dropDownList}
                                value={listSearchID}
                                onSelect={onDropListChange}
                            />
                        </div>
                        {
                            (isLoadingReport)
                            ?   <LoadingSpinner />
                            :   (receivedReport) 
                                ?   <DataTable content={receivedReport}/>
                                :   <h1>No report</h1>
                        }
                    </Grid>
                    <Grid
                        item
                        xs={16}
                        md={8}
                        bgcolor='rgb(192,192,192)'
                        sx={{
                            height: 582,
                            position: 'relative',
                            overflowY: 'auto',
                            minHeight: 582,
                            maxHeight: 675
                        }}
                    >
                        <div id="change-output">
                            <div id="bug-list">
                                {
                                    (isLoadingList)
                                    ?   <LoadingSpinner />
                                    :
                                    (receivedData.length > 0) ?
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
                                                                    <b>Bug ID:</b>{ key[0] }
                                                                </Typography>
                                                                <Typography>
                                                                    <b>Score:</b>{ data[key[0]] }
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
                                    (receivedItemReport)
                                    ?   <DataTable content={receivedItemReport} />
                                    :   <h1>No report found</h1>
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