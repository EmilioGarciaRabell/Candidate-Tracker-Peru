"use client";

import { useEffect, useState } from "react"
import "bulma/css/bulma.min.css";
import { Candidate } from "@/interfaces/CandidateInterface";
import { News } from "@/interfaces/News";


export default function Noticias(){
    const [candidates, setCandidates] = useState<Candidate[]>([])
    const [news, setNews] = useState<News[]>([])
    const [TIME, setTime] = useState("")

    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchCandidates = async () => {
        if (!apiUrl) {
          setError("La URL de la API no está configurada (NEXT_PUBLIC_API_URL).");
          setLoading(false);
          return;
        }
    
        setLoading(true);
        setError(null);
        try {
          const res = await fetch(`${apiUrl}/candidates`, { cache: "no-store" });
          if (!res.ok) throw new Error(`Error ${res.status}`);
          const data = await res.json();
          const list = (data.candidates ?? []) as Candidate[];
    
          setCandidates(list);
        } catch (err: any) {
          setError(err?.message || "Error al cargar candidatos");
        } finally {
          setLoading(false);
        }
      };



  const fetchNews = async () =>{
    if(!apiUrl){
        setError("error when fetching news")
        setLoading(false);
        return
    }

    setError(null)
    setLoading(true);

    try{
        const t = new Date()
        const hours = t.getHours()
        
        //in the morning display the morning news, in the evening change to evening news
   
        const timeParam = hours < 14 ? "morning" : "evening"; 
        const res = await fetch(`${apiUrl}/api/news/${timeParam}`)
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();
        const list = (data ?? []) as News[];
        setNews(list)
          
    }catch(err:any){
        setError(err?.message || "Error al cargar news");

    }finally{
        setLoading(false)
    }
  }

    function formatNews(news: News[], candidates: Candidate[]) {
        return news.map(n => {
            const candidate = candidates.find(c => c.id === n.id);
            return {
            ...n,
            candidate_name: candidate?.name, 
            };
        });
    }

useEffect(() => {
        fetchCandidates();
        fetchNews();
        const n = formatNews(news,candidates)
        setNews(n)
        // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


    return <>

        {news.map((n) => (
            <p key={n.id}>{n.id} - {n.news}</p>
        ))}
    </>
}