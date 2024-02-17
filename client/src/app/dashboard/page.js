'use client';

import { DonutChart, Grid, Card, Title, Flex, Text, Legend, BarChart, LineChart } from '@tremor/react';
import React, { useEffect, useState } from 'react';

export default function Dashboard() {
    const [complexity, setComplexity] = useState([]);
    const [semantics, setSemantics] = useState([]);
    const [topics, setTopics] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:3500/stats?parent_id=2&timeperiod_arg=Weekly`).then((res) => res.json()).then((data) => {
            setComplexity([
            ]);
            setSemantics([
                // { name: 'Positive', value: data.semantics.positive },
                // { name: 'Neutral', value: data.semantics.neutral },
                // { name: 'Negative', value: data.semantics.negative }
                { name: 'Positive', value: 0.1 },
                { name: 'Neutral', value: 0.2 },
                { name: 'Negative', value: 0.7 }
            ]);
            setTopics(
                Object.keys(data.topics).map((e, i) => {
                    return { name: e, 'Number of occurrences': data.topics[e] }
                })
            );
        });
    }, []);

    return (
        <main className="p-4 md:p-10 mx-auto max-w-7xl">
            <Grid numItems={4} className="gap-6">
                <Card className='max-w-ws'>
                    <Title>Sentiments</Title>
                    <DonutChart data={semantics} colors={['blue', 'cyan', 'indigo']} showLabel={false} className='py-4' />
                    <Legend
                        categories={['Positive', 'Neutral', 'Negative']}
                        colors={['blue', 'cyan', 'indigo']}
                        className="mt-3"
                    />
                </Card>
                <Card className='max-w-ws'>
                    <Title>Topics</Title>
                    <BarChart data={topics} className='mt-6' index='name' colors={['blue']} categories={['Number of occurrences']} yAxisWidth={30} />
                </Card>
                <Card className='max-w-ws'>
                    <Title>Language Complexity</Title>
                    <LineChart data={complexity} className='mt-6' index='name' colors={['blue']} categories={['Language complexity']} yAxisWidth={30} />
                </Card>
            </Grid>
        </main>
    );
}