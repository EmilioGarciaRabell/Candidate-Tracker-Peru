"use client";

import { useEffect, useState } from "react"
import "bulma/css/bulma.min.css";
import { Candidate } from "@/interfaces/CandidateInterface";
import { News } from "@/interfaces/News";
import s from "./noticias.module.css";



export default function Noticias(){
    const [candidates, setCandidates] = useState<Candidate[]>([])
    const [news, setNews] = useState<News[]>([])
    const [TIME, setTime] = useState("")

    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    function formatNews(news: News[], candidates: Candidate[]) {
        return news.map(n => {
            const candidate = candidates.find(c => c.id === n.id);
            return {
            ...n,
            name: candidate?.name, 
            };
        });
    }
    const loadData = async () => {
        if (!apiUrl) {
          setError("La URL de la API no está configurada (NEXT_PUBLIC_API_URL).");
          setLoading(false);
          return;
        }
    
        setLoading(true);
        setError(null);
        try {
        
          const t = new Date()
          const hours = t.getHours()
          console.log(hours)
          const timeParam = hours < 14 ? "morning" : "evening"; 
          const [candidatesRes, newsRes] = await Promise.all([
                fetch(`${apiUrl}/candidates`),
                fetch(`${apiUrl}/api/news/${timeParam}`),
          ]);

          //feth candidates
          const data = await candidatesRes.json();
          const list = (data.candidates ?? []) as Candidate[];

          //fetch news
            const newsdata = await newsRes.json();
            const newslist = (newsdata ?? []) as News[];

            const newsformat = formatNews(newslist,list)

            setCandidates(list);
            setNews(newsformat)

        } catch (err: any) {
          setError(err?.message || "Error al cargar candidatos");
        } finally {
          setLoading(false);
        }
      };


//add candidates with news at the top

useEffect(() => {
        loadData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
        console.log(news)
  }, []);

   useEffect(() => {
    if (news) {
      console.log('Updated API data in state:', news); // Log after state update
    }
  }, [news]); // Run when apiData changes

    const [openIndex, setOpenIndex] = useState(0)

    const toggle = (i: number) => {
    setOpenIndex(openIndex === i ? 0 : i);
  };

  return (
    <section className={s.pageBg}>
      <div className="container">
        <ul className={s.grid} role="list">
          {news?.map((n, i) => (
            <li key={i} className={s.gridItem} role="listitem">
              <div className={s.dropdown}>
                <button
                  className={s.dropdownHeader}
                  onClick={() => toggle(i)}
                >
                  <span>{n.name}</span>
                  <span className={s.count}>{n.news.length}</span>

                  <span
                    className={`${s.caret} ${
                      openIndex === i ? s.open : ""
                    }`}
                  >
                    +
                  </span>
                </button>

                <div
                  className={`${s.dropdownBody} ${
                    openIndex === i ? s.show : ""
                  }`}
                >
                  {n.news?.map((item, j) => (
                    <a key={j} href={item.link} className={s.dropdownItem}>
                      {item.title}
                    </a>
                  ))}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}