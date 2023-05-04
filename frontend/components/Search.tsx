'use client'

import { useState } from 'react';

import Results from './Results'
import Input from './Input'
import Relevancy from './Relevancy';


function Search() {

    const [rawResults, setRawResults] = useState([]);
    const [query, setQuery] = useState("");
    const [size, setSize] = useState(10);
    const [calculationTime, setCalculationTime] = useState(0.0);
    const [totalDocuments, setTotalDocuments] = useState(0);
    const [relevancy, setRelevancy] = useState("");
    const [isUserQuery, setIsUserQuery] = useState(false);

    const searchForSimilar = async(id: string) => {
        const response = await fetch(
            `/api/search-by-id/?id=${id}&k=${size}`
        );
        const data = await response.json();
        setRawResults(data.results);
        setQuery(`documents similar to ${id}`)
        setCalculationTime(data.time)
        setTotalDocuments(data.total)
        setIsUserQuery(false);
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
                setIsUserQuery={setIsUserQuery}
                setSize={setSize}
                size={size}
                setCalculationTime={setCalculationTime}
                setTotalDocuments={setTotalDocuments}
                setRelevancy={setRelevancy}
            />
            <div>
                <Relevancy
                    query={query}
                    size={size}
                    isUserQuery={isUserQuery}
                    rawResults={rawResults}
                    relevancy={relevancy}
                    setRelevancy={setRelevancy}                    
                />
            </div>
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