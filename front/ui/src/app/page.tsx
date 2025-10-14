import Image from "next/image";
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <main className="-mt-60 max-w-6xl mx-auto px-6 py-20 flex flex-col md:flex-row items-start gap-12 ">
      <div className="flex-1 flex flex-col items-start text-left space-y-6 h-80 gap-5">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight">Por un Peru informado en miras a las elecciones 2026</h1>
        <p className="text-lg md:text-xl text-gray-600 max-w-xl">Aprende sobre los candidatos, sus propuestas y mas</p>
        <div className="flex flex-row gap-12">
          <Link href={"/candidates"}>
                    <button className="button">Informate ahora</button>
          </Link>
           <Link href={"/"}>
               <button className="button">Conocenos</button>
           </Link>
        </div>
      </div>

      <div className="flex-1 flex justify-center">
        <Image 
        src={"/landing_page.jpg"} 
        alt={"imagen del landing page"}
        width={2000}
        height={2000}
        className="rounded-xl shadow-lg"
        ></Image>
        </div>
        </main>
        <footer className="">
        
        </footer>
      </div>
  );
}
