import Link from 'next/link'
import Image from "next/image";


export default function Navbar(){
    return (
        <header className='header'>
            <div className='div1'>
                <div className="navflex">

                    <div className='logo'>
                        <Link href="/" className="flex">
                            <Image 
                            src="/logo.svg"
                            alt="imagen del landing page"
                            width={70}
                            height={70}
                            className="cursor-pointer hover:scale-105 transition-transform duration-200"
                            >
                            </Image>
                        </Link>
                    </div>

                    <div className="links">
                            <Link href="/candidates" className="nav-link">Candidatos</Link>
                            <Link href="/candidates" className="nav-link">Noticias</Link>
                            <Link href="/dashboard" className="nav-link">Tendencias</Link>
                    </div>

                  <a href="#" title="" className="hidden lg:inline-flex items-center justify-center px-5 py-2.5 text-base transition-all duration-200 hover:bg-red-400 hover:text-black focus:text-black focus:bg-yellow-400 font-semibold text-white bg-black rounded-full" role="button"> Explora ahora </a>

                </div>
        </div>
        </header>
    )
}