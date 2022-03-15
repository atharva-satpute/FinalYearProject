import { FormControl, MenuItem, Select } from "@mui/material";
import React, { useState } from "react";

const DropDownBox = (props) => {
    const [selectID, setSelectID] = useState("");
    return(
        <FormControl sx={{ minWidth: 120 }}>
            <Select
                value={selectID}
                autoWidth
                displayEmpty
                inputProps={{ 'aria-label': 'Without label' }}
                sx={{ height:40 }}
                onChange={(event) => {
                    setSelectID(event.target.value)
                    props.onSelect(event)
                }}
            >
                <MenuItem value="" disabled>None</MenuItem>
                {
                    (props.bugList.length > 0) &&
                    (
                        props.bugList.map((id) => { 
                            return(
                                <MenuItem key={id} value={id}>{id}</MenuItem>
                            );
                        })
                    )
                }
            </Select>
        </FormControl>
    );
}
export default DropDownBox;