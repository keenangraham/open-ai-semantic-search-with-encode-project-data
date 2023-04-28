import { NextResponse } from 'next/server'


export async function GET(request: Request) {
    const BACKEND_URL = process.env.BACKEND_URL;
    const params = new URL(request.url);
    const response = await fetch(
      `${BACKEND_URL}/search-by-id/${params.search}`,
      {
        cache: 'no-store'
      }
    )
    const data = await response.json()
    return NextResponse.json(data)
  }