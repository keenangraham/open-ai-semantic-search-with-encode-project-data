import { NextResponse } from 'next/server'


export async function GET(request: Request) {
    const params = new URL(request.url);
    const response = await fetch(
      `http://backend:8000/search-by-id/${params.search}`,
      {
        cache: 'no-store'
      }
    )
    const data = await response.json()
    return NextResponse.json(data)
  }