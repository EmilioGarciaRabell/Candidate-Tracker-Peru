export default function Navbar(){
    return (
        <div>
            <nav className="flex justify-between items-center px-8 py-8 bg-white shadow-md ">
                <h1 className="text-2xl font-bold text-black">Perú 2026</h1>
            <div className="flex gap-6 text-gray-700 font-medium">
                <button className="hover:text-blue-600 transition text-xl">Perfiles de Candidatos</button>
                <button className="hover:text-blue-600 transition text-xl">Noticias y Actualidad Política</button>
                <button className="hover:text-blue-600 transition text-xl">Opinión Pública y Tendencias</button>
            </div>
            </nav>
        </div>
    )
}