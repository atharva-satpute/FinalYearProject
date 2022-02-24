import React, {useState} from "react";
import { useNavigate } from 'react-router-dom';
import { AppBar, Box, Button, IconButton, Menu, MenuItem, Toolbar, Typography } from '@mui/material'
import AccountCircle from '@mui/icons-material/AccountCircle';

const Navbar = (props) => {

    const navigate = useNavigate();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleMenu = (event) => {
        setAnchorEl(event.currentTarget)
    }

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="sticky">
                <Toolbar>
                    <Typography
                        variant="h5"
                        sx={{ flexGrow: 1 }}
                    >
                        Duplicate Bugs
                    </Typography>

                    {
                        !props.authCheck ?
                        (
                            <>
                                <Button 
                                    color="inherit"
                                    onClick={() => navigate("/signIn")}
                                >
                                    Sign In
                                </Button>
                                <Button
                                    color="inherit"
                                    onClick={() => navigate("/signUp")}
                                >
                                    Sign Up
                                </Button>
                            </>
                        )
                        :
                        (
                            <>
                                <IconButton 
                                    size="large"
                                    aria-label="account of current user"
                                    aria-controls="account-menu"
                                    aria-haspopup="true"
                                    onClick={handleMenu}
                                >
                                    <AccountCircle/>
                                </IconButton>
                                <Menu
                                    id="account-menu"
                                    anchorEl={anchorEl}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right'
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={Boolean(anchorEl)}
                                    onClose={handleClose}
                                >
                                    <MenuItem>Sign Out</MenuItem>
                                </Menu>
                            </>
                        )
                    }
                </Toolbar>
            </AppBar>
        </Box>
        
    );
}

export default Navbar;