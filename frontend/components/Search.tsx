'use client'

import { useState } from 'react';

import Results from '../components/Results'
import Input from '../components/Input'


function Search() {

    const [rawResults, setRawResults] = useState([]);
    const [query, setQuery] = useState("");
    const [size, setSize] = useState(10);
    const [calculationTime, setCalculationTime] = useState(0.0);
    const [totalDocuments, setTotalDocuments] = useState(0);

    const searchForSimilar = async(id: string) => {
        const response = await fetch(
            `/api/search-by-id/?id=${id}&k=${size}`
        );
        const data = await response.json();
        setRawResults(data.results);
        setQuery(`documents similar to ${id}`)
        setCalculationTime(data.time)
        setTotalDocuments(data.total)
        window.scrollTo(
            {
                top: 0,
                behavior: "smooth",
            }
        );
    }

    return (
        <div>
            <Input
                setRawResults={setRawResults}
                setQuery={setQuery}
                setSize={setSize}
                size={size}
                setCalculationTime={setCalculationTime}
                setTotalDocuments={setTotalDocuments}
            />
            <div className='mx-0'>
                <Results
                    rawResults={rawResults}
                    query={query}
                    totalDocuments={totalDocuments}
                    calculationTime={calculationTime}
                    searchForSimilar={searchForSimilar}
                />
            </div>
        </div>
    )
}

export default Search