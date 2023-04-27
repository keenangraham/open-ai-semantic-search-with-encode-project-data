'use client'

import Link from "next/link"


type Result = {
    id: string;
    score: number;
    document: any;
}

interface ResultsProps {
    rawResults: Result[],
    query: string
}


function Title(query: string, numberOfResults: number) {
    return (
        <div className="italic font-bold pb-4 px-0 md:px-11 text-justify">
            Showing <span className="not-italic text-violet-500">{numberOfResults}</span> results for <span className="not-italic text-violet-500">{query}</span>
        </div>
    )
}


function Results(props: ResultsProps) {
  
  return (
    <div>
        {props.query && Title(props.query, props.rawResults.length)}
        <div className='grid gap-4 grid-cols-1 px-0 md:px-10'>

            {
                props.rawResults?.map(
                    (result, i: number) => (
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
                                {result.document.description && <div>Description: <span className="font-light">{result.document.description}</span></div>}
                            </div>
                        </div>
                    )
                )
            }
        </div>
    </div>
  )
}

export default Results