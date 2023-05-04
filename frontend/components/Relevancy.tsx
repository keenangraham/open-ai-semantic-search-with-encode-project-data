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


interface evaluateRelevancyProps {
    query: string;
    rawResults: Result[];
    signal: AbortSignal;
}


async function evaluateRelevancy(
    {
        query,
        rawResults,
        signal,
    }: evaluateRelevancyProps
) {
    const response = await fetch(
        '/api/evaluate-search-relevancy/',
        {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          cache: 'no-store',
          signal: signal,
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
            const controller = new AbortController();
            let ignore = false;
            if (!props.isUserQuery || props.query.length === 0) {
                return
            }
            setIsLoading(true)
            props.setRelevancy("")
            evaluateRelevancy(
                {
                    query: props.query,
                    rawResults: props.rawResults,
                    signal: controller.signal,
                }
            ).then(
                result => {
                    if (ignore) {
                        return
                    }
                    props.setRelevancy(result.evaluation)
                    setIsLoading(false)
                }
            )
            return () => {
                ignore = true;
                controller.abort();
            }
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