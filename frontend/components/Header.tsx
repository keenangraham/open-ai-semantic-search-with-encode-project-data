import Image from "next/image"
import Link from "next/link"


function Header() {
  return (
    <header className="flex p-5 justify-between sticky top-0 bg-white z-50 shadow-md">
        <div className="flex space-x-2 items-center">
            <Image
                src="/../public/embeddings.png"
                alt="logo"
                height={60} 
                width={60} 
            />
            <div className="p-2">
                <h1 className="font-bold">
                    Semantic search of <span className="text-violet-500">ENCODE project</span> data
                </h1>
                <h2 className="text-xs">
                    Using OpenAI embeddings from the <span className="bg-violet-500 text-white font-bold">text-embedding-ada-002</span> model
                </h2>
            </div>
        </div>
        <div className="flex text-xs md:text-base divide-x items-center text-gray-500">
            <Link 
                href="https://www.encodeproject.org"
                className="px-2 font-light text-right"
            >
                Data
            </Link>
            <Link 
                href="https://github.com/keenangraham/open-ai-semantic-search-with-encode-project-data"
                className="px-2 font-light"
            >
                Github
            </Link>
        </div>
    </header>
  )
}

export default Header