import Image from "next/image";
import { Candidate } from "@/interfaces/CandidateInterface";

export default function UserCard({name,party,Age,ideology,education,image,summary}:Candidate){

    return (<>
        <div className="
              flex relative p-10 rounded-xl  bg-white/50  max-w-md m-4  shadow-[0_0_30px_rgba(0,0,0,0.15)] overflow-hidden 
                ">
            <div className="text-black ml-[1.5rem]">
                <div className="flex flex-row gap-30">
                    <div className="mt-15">
                    <h2 className="text-4xl">{name}</h2>
                    <h4 className="text-2xl">{party}</h4>
                    </div>
                <div className="mt-8 max-w-full block mb-10">
                    <Image 
                    src={image} 
                    alt={"candidate_image"}
                    width={500}
                    height={500}
                    className="shadow-lg rounded-full"
                    ></Image>
                </div>
                </div>
                <p className="text-[0.9rem] mb-10 ">
                    Informacion: {summary}
                </p>
                <ul className="flex mb-[1rem] gap-3">
                    <li className="min-w-20">
                        <h3 className="text-[0.99rem]">{Age.toString()}</h3>
                        <h4 className="text-[0.75rem]" >Edad </h4>
                    </li>
                    <li className="min-w-20">
                        <h3 className="text-[0.99rem]">{education}</h3>
                        <h4 className="text-[0.75rem]">Educacion </h4>
                    </li>
                </ul>
                <div className="justify-center mt-10">
                    <button className="button">Mas Info</button>
                    {/* <button className="button">Propuestas</button> */}
                </div>
            </div>
        </div>

    </>)
}