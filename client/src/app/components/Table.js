"use client";

import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, getKeyValue, Spinner } from "@nextui-org/react";

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
        key: "reasoning",
        label: "Reasoning",
    },
];

export default function ConversationTable({ data }) {
    return (
        <Table isStriped aria-label="Conversation Table">
            <TableHeader columns={columns}>
                {(column) => <TableColumn key={column.key}>{column.label}</TableColumn>}
            </TableHeader>
            <TableBody items={data} emptyContent={"No rows to display."} loadingContent={<Spinner label="Loading..." />}>
                {(item) => (
                    <TableRow key={item.question}>
                        {(columnKey) => <TableCell>{getKeyValue(item, columnKey)}</TableCell>}
                    </TableRow>
                )}
            </TableBody>
        </Table>
    );
}