import { NextResponse } from 'next/server'


export async function POST(request: Request) {
    const body = await request.json();
    const BACKEND_URL = process.env.BACKEND_URL;
    const response = await fetch(
      `${BACKEND_URL}/evaluate-search-relevancy/`,
      {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-store',
        body: JSON.stringify(body),
      }
    )
    const data = await response.json()
    return NextResponse.json(data)
  }