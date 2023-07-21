'use client'
import Link from 'next/link';
import React from 'react';

async function search_all(term: string) {
    const url = `http://127.0.0.1:5000/search/${term}`;
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

export default function Search({ params }: { params: { query: string } }) {
  const term = params.query;  
  const [search, setSearch] = React.useState(params.query);
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
      setResults([]);
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
            <div className="w-5/6 mt-3">
                {results.length != 0 &&
                    results.map((result: any) => (
                        <div
                        key={result.hash}
                        onClick={
                          () => {
                            window.location.href = `/patient/${result.hash}`;
                          }
                        }
                            className="p-4 my-4 cursor-pointer text-xl border-2 leading-relaxed rounded-lg hover:scale-105 transform transition-all duration-200 ease-in-out"
                        >
                            <p className="py-1">
                                Patient Name:{' '}
                                <span className="bg-green-200">
                                    {result.name}
                                </span>
                            </p>
                            <p className="py-1">
                                Treated By:{' '}
                                <Link
                                    href={'/docter/' + result.doctor}
                                    className="underline"
                                >
                                    {result.doctor}
                                </Link>
                            </p>
                            <p className="py-1">
                                Visited on:{' '}
                                <span className="">
                                    {new Date(result.time).toDateString()}
                                </span>
                            </p>
                            <p className="py-0.5">
                          Problems: {
                            result.problems
                          }
                            </p>
                        </div>
                    ))}
                {results.length == 0 && <p>No results found</p>}
            </div>
        </div>
    );
}
