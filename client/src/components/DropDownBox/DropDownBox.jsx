import { FormControl, MenuItem, Select } from "@mui/material";
import React from "react";

const DropDownBox = (props) => {
    return(
        <FormControl sx={{ minWidth: 120 }}>
            <Select
                value={props.value}
                autoWidth
                displayEmpty
                inputProps={{ 'aria-label': 'Without label' }}
                sx={{ height:40 }}
                onChange={(event) => {
                    props.onSelect(event)
                }}
            >
                {
                    (props.bugList.length > 0) ?
                    (
                        props.bugList.map((id) => { 
                            return(
                                <MenuItem key={id} value={id}>{id}</MenuItem>
                            );
                        })
                    )
                    :
                    <MenuItem value="" disabled>None</MenuItem>
                }
            </Select>
        </FormControl>
    );
}
export default DropDownBox;