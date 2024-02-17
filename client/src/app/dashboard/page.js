'use client';

import { DonutChart, Grid, Card, Title, Flex, Text } from '@tremor/react';
import React, { useEffect, useState } from 'react';

export default function Dashboard() {
    const [complexity, setComplexity] = useState({});
    const [semantics, setSemantics] = useState({});
    const [topics, setTopics] = useState({});

    useEffect(() => {
        fetch('http://localhost:3500/stats').then((res) => res.json()).then((data) => {
            setComplexity(data.complexity);
            setSemantics(data.semantics);
            setTopics(data.topics);
        });
    }, []);

    return (
        <main className="p-4 md:p-10 mx-auto max-w-7xl">
            <Grid numItems={4} className="gap-6">
                {JSON.stringify(complexity)}
                {JSON.stringify(semantics)}
                {JSON.stringify(topics)}
                {/* {data.map((item) => (
                    <Card key={ }>
                    </Card>
                ))} */}
                {/* <Title>{item.category}</Title>
<Flex
    justifyContent="start"
    alignItems="baseline"
    className="space-x-2"
>
    <Metric>{item.stat}</Metric>
    <Text>Total views</Text>
</Flex>
<Flex className="mt-6">
    <Text>Pages</Text>
    <Text className="text-right">Views</Text>
</Flex> */}
            </Grid>
        </main>
    );
}

// const website = [
//     { name: '/home', value: 1230 },
//     { name: '/contact', value: 751 },
//     { name: '/gallery', value: 471 },
//     { name: '/august-discount-offer', value: 280 },
//     { name: '/case-studies', value: 78 }
// ];

// const shop = [
//     { name: '/home', value: 453 },
//     { name: '/imprint', value: 351 },
//     { name: '/shop', value: 271 },
//     { name: '/pricing', value: 191 }
// ];

// const app = [
//     { name: '/shop', value: 789 },
//     { name: '/product-features', value: 676 },
//     { name: '/about', value: 564 },
//     { name: '/login', value: 234 },
//     { name: '/downloads', value: 191 }
// ];

// const data = [
//     {
//         category: 'Website',
//         stat: '10,234',
//         data: website
//     },
//     {
//         category: 'Online Shop',
//         stat: '12,543',
//         data: shop
//     },
//     {
//         category: 'Mobile App',
//         stat: '2,543',
//         data: app
//     }
// ];