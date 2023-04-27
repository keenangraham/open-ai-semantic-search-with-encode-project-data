'use client'

import { useState } from 'react';

import Results from '../components/Results'
import Input from '../components/Input'



function Search() {

    const [rawResults, setRawResults] = useState([]);
    const [query, setQuery] = useState("");

  return (
    <div>
        <Input setRawResults={setRawResults} setQuery={setQuery} />
        <div className='mx-0'>
            <Results rawResults={rawResults} query={query} />
        </div>
    </div>
  )
}

export default Search