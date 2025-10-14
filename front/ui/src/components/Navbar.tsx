import Link from 'next/link'

export default function Navbar(){
    return (
        <div>
            <nav className="flex justify-between items-center px-8 py-8 bg-white shadow-md ">
                <Link href="/" className="text-2xl font-bold text-black">Perú 2026</Link>
            <div className="flex gap-6 text-gray-700 font-medium">
                <Link href="/candidates" className="hover:text-blue-600 transition text-xl">Perfiles de Candidatos</Link>
                <Link href="/candidates" className="hover:text-blue-600 transition text-xl">Noticias y Actualidad Política</Link>
                <Link href="/candidates" className="hover:text-blue-600 transition text-xl">Opinión Pública y Tendencias</Link>
            </div>
            </nav>
        </div>
    )
}