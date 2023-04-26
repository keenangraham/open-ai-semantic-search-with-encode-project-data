import { NextResponse } from 'next/server'


export async function GET(request: Request) {
    /*const response = await fetch(
      'http://backend:8000/search-by-query/?query=crispr&k=3',
      {
        cache: 'no-store'
      }
    )
    const data = await response.json()
    return NextResponse.json(data)
    */
    return new Response('Okay')
  }
  