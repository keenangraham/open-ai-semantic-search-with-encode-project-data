'use client'


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
                    result => (
                        <div key={result.id} className="w-full shadow-2xl drop-shadow-lg rounded-sm bg-gray-50 p-4">
                            <div>ID: <span>{result.id}</span></div>
                            <div>Score: <span className="text-violet-500 text-bold">{result.score}</span></div>
                            {result.document.title && <div>Title: <span className="font-bold">{result.document.title}</span></div>}
                            <div>Description: <span className="font-light">{result.document.description}</span></div>
                        </div>
                    )
                )
            }
        </div>
    </div>
  )
}

export default Results