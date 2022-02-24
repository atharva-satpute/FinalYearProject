import React from "react";
import { Avatar, Box, Button, Container, CssBaseline, Link, TextField, Typography } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

class SignIn extends React.Component {

    render() {
        return(
            <Container component={'main'} maxWidth={'xs'}>
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center'
                    }}
                >
                    <Avatar sx={{ m:1,bgcolor: 'secondary.main' }} >
                        <LockOutlinedIcon/>
                    </Avatar>

                    <Typography component={'h1'} variant={'h5'}>
                        Sign In
                    </Typography>
                    
                    {/* Sign In Form */}
                    <Box
                        component={'form'}
                        sx={{mt:1}}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                        />

                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type={'password'}
                            id="password"
                            autoComplete="current-password"
                        />

                        {/* Sign In Button */}
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2}}
                        >
                            Sign In
                        </Button>

                        {/* Sign Up Redirect */}
                        <Link href="/signUp" variant="body2">
                            {"Don't have an account? Sign Up"}
                        </Link>
                    </Box>
                </Box>
            </Container>
        );
    }
}

export default SignIn;