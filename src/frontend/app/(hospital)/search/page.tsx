'use client';
import React from 'react';

async function search_all(term: string) {
    const url = `http://127.0.0.1:5000/search/${term}`;
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

export default function SearchPage({ }:any) {
    const term = '';
    const [search, setSearch] = React.useState(term);
    const [results, setResults] = React.useState([]);

    React.useEffect(() => {
        setSearch(term);
        const data = async () => {
            const data = await search_all(term);
            setResults(data);
        };
        data();
    }, [term]);

    const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        let { value } = e.target;
        if (value == '') {
            setResults([]);
            setSearch('');
            return;
        }
        setSearch(value);
        const data = await search_all(value);
        setResults(data);
    };

    return (
        <div className="flex flex-col py-3 justify-center items-center">
            <div className="w-5/6 focus:outline-none">
                <input
                    type="text"
                    className="text-lg w-full border-2 border-black rounded-md focus:outline-none p-4 rounded-"
                    value={search}
                    onChange={handleChange}
                />
            </div>
            <div className="w-5/6">
                {results.length != 0 && JSON.stringify(results)}
                {results.length == 0 && <p>No results found</p>}
            </div>
        </div>
    );
}
