import React from "react";
import { Avatar, Box, Button, Container, CssBaseline, Grid, Link, TextField, Typography } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';

class SignUp extends React.Component {
    
    render() {
        return(
            <Container component={'main'} maxWidth={'xs'}>
                <CssBaseline/>
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center'
                    }}
                >
                    <Avatar sx={{ m:1, bgcolor: 'secondary.main'}}>
                        <LockOutlinedIcon/>
                    </Avatar>
                    
                    <Typography component="h1" variant="h5">
                        Sign Up
                    </Typography>

                    {/* Sign Up Form */}
                    <Box component={'form'} sx={{ mt: 3}}>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    name="firstName"
                                    required
                                    fullWidth
                                    id="firstName"
                                    label="First Name"
                                    autoFocus
                                />
                            </Grid>

                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    fullWidth
                                    id="lastName"
                                    label="Last Name"
                                    name="lastName"
                                />
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    id="email"
                                    label="Email Address"
                                    name="email"
                                />
                            </Grid>

                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    name="password"
                                    label="Password"
                                    type="password"
                                    id="password"
                                    autoComplete="new-password"
                                />
                            </Grid>
                        </Grid>

                        {/* Sign Up Button */}
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt:3, mb: 2}}
                        >
                            Sign Up
                        </Button>

                        {/* Sign In Redirect */}
                        <Link href="/signIn" variant="body2">
                            Already have an account? Sign in
                        </Link>
                    </Box>
                </Box>
            </Container>
        );
    }
}
export default SignUp;