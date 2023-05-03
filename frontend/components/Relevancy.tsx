'use client'

import { useEffect, useState, Dispatch, SetStateAction, } from 'react';

import type { Result } from "../components/Results"


interface RelvancyProps {
    query: string;
    size: number;
    isUserQuery: boolean;
    rawResults: Result[];
    relevancy: string;
    setRelevancy: Dispatch<SetStateAction<string>>;
}


async function evaluateRelevancy(query: string, rawResults: Result[]) {
    const response = await fetch(
        '/api/evaluate-search-relevancy/',
        {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          cache: 'no-store',
          body: JSON.stringify(
            {
                query: query,
                results: rawResults.map(r => r.document)
            }
          ),
        }
      )
      return await response.json()
}


function Relevancy(props: RelvancyProps) {

    const [isLoading, setIsLoading] = useState(false);

    useEffect(
        () => {
            if (!props.isUserQuery || props.query.length === 0) {
                return
            }
            setIsLoading(true)
            props.setRelevancy("")
            evaluateRelevancy(
                props.query,
                props.rawResults,
            ).then(
                result => props.setRelevancy(result.evaluation)
            ).finally(
                () => {
                    setIsLoading(false)
                }
            )
        },
        [
            props.rawResults
        ]
    )

    return (
        (
            props.isUserQuery &&
            <div className="italic font-light text-justify border-2 border-violet-100 m-10 p-10 rounded-lg flex flex-col gap-4">
                {
                    isLoading
                    ? <div className="text-center animate-pulse">
                        Determining search relevancy with <span className="bg-violet-100 text-violet-500">gpt-3.5-turbo</span>                    
                    </div>
                    : <div>
                        <div className="">
                            <span className="bg-violet-100 text-violet-500">gpt-3.5-turbo</span>: {props.relevancy}
                        </div>
                    </div>
                }
            </div>   
        ) || <div></div>
    )
}


export default Relevancy