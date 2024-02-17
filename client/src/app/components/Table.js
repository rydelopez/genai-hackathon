"use client";

import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, getKeyValue } from "@nextui-org/react";

const columns = [
    {
        key: "question",
        label: "Question",
    },
    {
        key: "answer",
        label: "Answer",
    },
    {
        key: "ranking",
        label: "Ranking",
    },
    {
        key: "reason",
        label: "Reason",
    },
];

export default function ConversationTable({ data }) {
    return (
        <Table>
            <TableHeader columns={columns}>
                {(column) => <TableColumn key={column.key}>{column.label}</TableColumn>}
            </TableHeader>
            <TableBody items={data}>
                {(item) => (
                    <TableRow>
                        {(columnKey) => <TableCell>{getKeyValue(item, columnKey)}</TableCell>}
                    </TableRow>
                )}
            </TableBody>
        </Table>
    );
}