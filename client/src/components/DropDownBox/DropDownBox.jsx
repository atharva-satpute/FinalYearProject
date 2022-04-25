import { FormControl, MenuItem, Select } from "@mui/material";
import React from "react";

const DropDownBox = (props) => {
    return(
        <FormControl sx={{ minWidth: 120 }}>
            <Select
                value={props.value}
                autoWidth
                displayEmpty
                disabled={(props.bugList.length === 0) ? true: false}
                inputProps={{ 'aria-label': 'Without label' }}
                MenuProps={{ style: { maxHeight: 400 }}}
                sx={{ height: 40 }}
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