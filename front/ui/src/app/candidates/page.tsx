'use client'; 
import UserCard from "@/components/UserCard";
import { Candidate } from "@/interfaces/CandidateInterface";
import { useEffect, useState } from "react";
import s from "./candidates.module.css"
export default function Candidates() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    const fetchCandidates = async () => {
      try{
        const baseUrl = process.env.NEXT_PUBLIC_API_URL
        const res = await fetch(`${apiUrl}/candidates`
          
        )
        console.log(res)
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        

        setCandidates(data.candidates)

        } catch (err: any) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      
    }

    fetchCandidates()

  },[])

  if (loading) return <p>Loading...</p>;


  return (
    <div className={s.candidates_list}>
        {candidates.map((c: Candidate) => (
          <li key={c.id}>
            <UserCard {...c}></UserCard>
          </li>
        ))}
    </div>
  );
}

