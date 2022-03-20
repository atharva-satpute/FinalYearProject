import React from "react";
import { AppBar, Box, Toolbar, Typography } from '@mui/material';

const Navbar = () => {

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
                </Toolbar>
            </AppBar>
        </Box> 
    );
}
export default Navbar;