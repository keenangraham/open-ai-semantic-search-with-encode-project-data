'use client'

import { useState, useEffect } from 'react';

import Link from "next/link"

import type { Result } from "../components/Results"


interface CardProps{
    result: Result,
    searchForSimilar: (id: string) => void
};

const DETAIL_LIMIT = 750;

const renderDetails = (details: string, showDetails: boolean): string => {
    if (showDetails === true || details.length <= DETAIL_LIMIT) {
        return details;
    }
    return details.slice(0, DETAIL_LIMIT) + "...";
};


function Card(props: CardProps) {

    const [showDetails, setShowDetails] = useState(false);

    const result = props.result;

    useEffect(
        ()=>{
            setShowDetails(false);
        },
        [props.result]
    )

    return (
        <div
            key={result.id}
            className="w-full shadow-2xl drop-shadow-lg rounded-sm p-10 bg-gray-50 hover:bg-violet-50"
        >
            <div className="flex flex-col gap-y-2">
                <div>
                    ID: <Link className="underline" href={`https://www.encodeproject.org${result.id}`} rel="noopener noreferrer" target="_blank">{result.id}</Link>
                </div>
                {result.document.title && <div>Title: <span className="font-bold">{result.document.title}</span></div>}
                <div>Score: <span className="text-violet-500 text-bold">{result.score.toFixed(7)}</span></div>
                {result.document.pi && <div>Lab: <span className="font-light">{result.document.pi.title}</span></div>}
                {
                result.document.description && 
                <div>
                    Description: <span className="font-light">{renderDetails(result.document.description, showDetails)}</span> 
                </div>
                }
                <div className='flex justify-between'>
                    <div>
                        <button type="button" onClick={() => setShowDetails(!showDetails)} className="p-2 pl-0 text-violet-500 font-bold text-sm">{showDetails ? 'Less' : 'More'}</button>
                    </div>
                    <div className={`${(showDetails !== true) ? 'hidden': ''}`}>
                        <button onClick={() => props.searchForSimilar(result.id)} type="button" className="border-2 p-2 border-violet-500 text-violet-500 text-sm rounded-full">Find simlar documents</button>
                    </div>
                </div>
            </div>
        </div>
    )
}


export default Card