import Image from "next/image";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <main className="max-w-6xl mx-auto px-6 py-20 flex flex-col md:flex-row items-start gap-12">
      <div className="flex-1 flex flex-col items-start text-left space-y-6 h-80 gap-8">
        <h1 className="text-6xl text-black">Por un Peru informado en miras a las elecciones 2026</h1>
        <p className="text-4xl text-black">Aprende sobre los candidatos, sus propuestas y mas</p>
        <div className="flex flex-row gap-12">
          <button className=" text-black font-semibold w-80 px-8 py-3 rounded-lg shadow hover:bg-gray-400 transition">Informate ahora</button>
           <button className=" text-black font-semibold w-80 px-8 py-3 rounded-lg shadow hover:bg-gray-400 transition">Aprende sobre nosotros</button>
        </div>
      </div>

      <div className="flex-1 flex justify-center">
        <Image 
        src={"/landing_page.jpg"} 
        alt={"imagen del landing page"}
        width={500}
        height={500}
        className="rounded-xl shadow-lg"
        ></Image>
        </div>
        </main>
        <footer className="">
        
        </footer>
      </div>
  );
}
