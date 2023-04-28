'use client'

import { Dispatch, SetStateAction } from "react"

import Card from "../components/Card"


export type Result = {
    id: string;
    score: number;
    document: any;
}

interface ResultsProps {
    rawResults: Result[],
    query: string,
    searchForSimilar: (id: string) => void
    totalDocuments: number
    calculationTime: number
}


function Title(query: string, numberOfResults: number, totalDocuments: number, calculationTime: number) {
    return (
        <div className="italic text-justify border-violet-500 m-10 mb-0 flex">
            <div className="border-violet-500 border-0 rounded-lg p-5 pl-0 pb-2">
                Showing <span className="not-italic bg-violet-500 text-white rounded-md p-1">{numberOfResults}</span> of {Intl.NumberFormat().format(totalDocuments)} results ({calculationTime.toFixed(5)} seconds) for <span className="not-italic text-violet-500">{query}</span>
            </div>
            <div>
            </div>
        </div>
    )
}


function Results(props: ResultsProps) {

  
  
  return (
    <div>
        {props.query && Title(props.query, props.rawResults.length, props.totalDocuments, props.calculationTime)}
        <div className='grid gap-4 grid-cols-1 px-0 md:px-10'>
            {
                props.rawResults?.map(
                    (result: Result) => <Card result={result} searchForSimilar={props.searchForSimilar} />
                )
            }
        </div>
    </div>
  )
}

export default Results;