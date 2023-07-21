import React from 'react'
import Auth from '@/app/(landing)/auth';

type Props = {}

async function getPatientData(hash: string) {
    const auth = await Auth();
    const response = await fetch(`http://127.0.0.1:5000/get/${hash}`, {
        method: 'POST',
        body: JSON.stringify({
            hash,
            doc_id: auth.doc_id,
            password: auth.password,
        }),
        headers: {
            'Content-Type': 'application/json',
        },
    });
    const data = await response.json();
    console.log(data);
    return data;
}

export default async function Patient({ params }: { params: { hash: string } }) {
    return (
        <>
            {
                JSON.stringify(await getPatientData(params.hash))
            }
        </>
    )
}