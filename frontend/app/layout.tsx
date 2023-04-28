import '../styles/globals.css';

import Header from '../components/Header';


export const metadata = {
  title: 'Semantic Search',
  description: 'Semantic search of ENCODE project data using OpenAI embeddings',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel='icon' href="/favicon.ico"></link>
      </head>
      <body>
        <Header />
        {children}
      </body>
    </html>
  )
}
