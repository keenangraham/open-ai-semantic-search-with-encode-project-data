'use client'

import { useState } from "react"

import useSWR from "swr";

import fetchSuggestion from "@/lib/fetchSuggestion";


function Input() {

    const [input, setInput] = useState('');
    
    const {data: suggestion, error, isLoading, mutate, isValidating} = useSWR(
        '/api/suggestion',
        fetchSuggestion,
        {
            revalidateOnFocus: false,
        }
    )
    console.log(suggestion)
    return (
        <div className="m-10">
            <form className="flex flex-col lg:flex-row shadow-md shadow-slate-400/10 border rounded-md lg:divide-x">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-1 p-4 outline-none rounded-md"
                    placeholder="Enter a query..."
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
                >
                    Use suggestion
                </button>
            </form>
        </div>
    )
}

export default Input