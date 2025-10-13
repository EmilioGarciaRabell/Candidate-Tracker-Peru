import Image from "next/image";
import { Candidate } from "@/interfaces/CandidateInterface";

export default function UserCard({name,party,Age,birthplace,ideology,education,image}:Candidate){

    return (<>
        <div className="bg-blue-400 rounded-lg shadow-md p-8 flex items-center">
            <div className="flex justify-center">
                    <Image 
                    src={image} 
                    alt={"candidate_image"}
                    width={200}
                    height={200}
                    className="rounded-xl shadow-lg"
                    ></Image>
            </div>
            <div className="text-black flex-1">
                <div>
                    {name}
                </div>
                <div>
                 {party}
                </div>
                <div>
                    {birthplace}
                </div>
                <div>
                    {ideology}
                </div>
                <div>
                    {education}
                </div>
            </div>
        </div>

    </>)
}