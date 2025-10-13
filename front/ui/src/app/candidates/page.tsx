import UserCard from "@/components/UserCard";
import { Candidate } from "@/interfaces/CandidateInterface";

export default function Candidates() {

  let candidate_array: Candidate[] = [
    {id:1,name:"Porky",party:"PPK",Age:81,birthplace:"cliclayo",education:"alas peruanas",ideology:"right-wing",image:"/landing_page.jpg"},
    {id:2,name:"Porky",party:"PPK",Age:81,birthplace:"cliclayo",education:"alas peruanas",ideology:"right-wing",image:"/landing_page.jpg"},
    {id:3,name:"Porky",party:"PPK",Age:81,birthplace:"cliclayo",education:"alas peruanas",ideology:"right-wing",image:"/landing_page.jpg"},
  ]

 
  return (
    <div className="flex flex-row items-center gap-5">
        {candidate_array.map((c: Candidate) => (
          <li key={c.id}>
            <UserCard {...c}></UserCard>
          </li>
        ))}
    </div>
  );
}
