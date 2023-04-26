'use client'

import { FormEvent, use, useState } from "react"

import useSWR from "swr";

import fetchSuggestion from "@/lib/fetchSuggestion";


function Input() {

    const [input, setInput] = useState("");
    
    const {data: suggestion, error, isLoading, mutate, isValidating} = useSWR(
        '/api/suggestion',
        fetchSuggestion,
        {
            revalidateOnFocus: false,
        }
    )

    const submitSearchByQuery = async(useSuggestion?: boolean) => {
        const userInput = input;
        setInput("");
        const query = useSuggestion ? suggestion : userInput;
        const response = await fetch(
            `/api/search-by-query/?query=${query}&k=3`
        );
        const data = await response.json();
        console.log(data);
    }

    const handleSubmit = async(e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        await submitSearchByQuery();
    };

    const loading = isValidating || isLoading;

    return (
        <div className="m-10">
            <form onSubmit={handleSubmit} className="flex flex-col lg:flex-row shadow-md shadow-slate-400/10 border rounded-md lg:divide-x">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-1 p-4 outline-none rounded-md"
                    placeholder={(loading && "Getting suggestion...") || suggestion || "Enter a query..."}
                />
                <button
                    className={
                        `p-4 font-bold 
                        ${
                            input
                              ? 'text-white bg-violet-500 transition-colors duration-200' 
                              : 'text-gray-300 cursor-not-allowed'
                        }`
                    }
                    type="submit"
                    disabled={!input}
                >
                    Search
                </button>
                <button 
                    className="p-4 bg-violet-400 text-white transition-colors-duration-200 font-bold
                    disabled:text-gray-300 disabled:cursor-not-allowed disabled:bg-gray-400"
                    type="button"
                    onClick={() => submitSearchByQuery(true)}
                >
                    Use suggestion
                </button>
                <button
                    className="p-4 bg-white text-violet-500 border-none transition-colors duration-200
                    rounded-b-md md:rounded-r-md md:rounded-bl-none font-bold"
                    type="button"
                    onClick={mutate}
                >
                    New Suggestion
                </button>
            </form>

            {
                input && (
                    <p className="italic pt-2 pl-2 font-light">
                        Suggestion: {" "}
                        <span className="text-violet-500">
                            {loading ? "Getting suggestion" : suggestion}
                        </span>
                    </p>
                )
            }
        </div>
    )
}

export default Input