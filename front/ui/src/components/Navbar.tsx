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
                            <Link href="/parties" className="nav-link">Partidos</Link>
                            <Link href="/candidates" className="nav-link">Noticias</Link>
                            <Link href="/dashboard" className="nav-link">Tendencias</Link>
                    </div>

                  <a href="#" title="" className="customButton hidden lg:inline-flex items-center justify-center " role="button"> Explora ahora </a>

                </div>
        </div>
        </header>
    )
}