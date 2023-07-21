'use client'
import React from 'react'

type Props = {}

export default async function LoginPage({ }: Props) {
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const doc_id = e.currentTarget.doc_id.value
        const password = e.currentTarget.password.value
        const response = await fetch('http://127.0.0.1:5000/signin', {
            method: 'POST',
            body: JSON.stringify({
                doc_id: doc_id,
                password: password,
            }),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        if (data) {
            document.cookie = `doc_id=${doc_id}`
            document.cookie = `password=${password}`
            window.location.href = '/'
        }
        console.log(data)
    }
    return (
        <>
            <div className="flex flex-col justify-center">
                <form onSubmit={handleSubmit}>
                    <div className='w-3/5'>
                        <input
                            type="text"
                            placeholder="Docter ID"
                            name="doc_id"
                            id="username"
                            className="border-2 border-black rounded-lg p-1"
                        />
                        <input
                            type="text"
                            placeholder="Password"
                            name="password"
                            id="password"
                            className="border-2 border-black rounded-lg p-1"
                        />
                        <button
                            type="submit"
                            className="bg-black text-white rounded-lg p-1"
                        >
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </>
    );
}