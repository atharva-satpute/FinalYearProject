import { Paper, Table, TableBody, TableCell, TableContainer, TableRow } from "@mui/material";
import React from "react";

const DataTable = (props) => {
    let data = props.content
    let keys = Object.keys(data)
    return(
        <TableContainer component={ Paper }>
            <Table>
                <TableBody>
                    {
                        keys.map((key) => {
                            return(
                                <TableRow key={key}>
                                    <TableCell>{ key }:</TableCell>
                                    <TableCell 
                                        sx={{
                                            whiteSpace: 'normal',
                                            wordBreak: 'break-word'
                                        }}
                                    >
                                        { data[key] }
                                    </TableCell>
                                </TableRow>
                            );
                        })
                    }
                </TableBody>
            </Table>
        </TableContainer>
    );
}
export default DataTable;