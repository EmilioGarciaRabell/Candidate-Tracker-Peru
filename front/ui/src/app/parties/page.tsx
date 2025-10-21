'use client'; 
import UserCard from "@/components/UserCard";
import { Party } from "@/interfaces/Party";
import { useEffect, useState } from "react";
import s from "./parties.module.css"
export default function Parties() {
  const [parties, setParties] = useState<Party[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    const fetchParties = async () => {
      try{
        const baseUrl = process.env.NEXT_PUBLIC_API_URL
        const res = await fetch(`${apiUrl}/parties`
          
        )
        console.log(res)
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        

        setParties(data.parties)

        } catch (err: any) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      
    }

    fetchParties()

  },[])

  if (loading) return <p>Loading...</p>;


  return (
    <div className={s.candidates_list}>
        {parties.map((c: Party) => (
          <li key={c.id}>
            <UserCard {...c}></UserCard>
          </li>
        ))}
    </div>
  );
}

