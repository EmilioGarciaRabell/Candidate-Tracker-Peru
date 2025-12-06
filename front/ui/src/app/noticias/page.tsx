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
    const currentNews = 3
    const [visibleNews, setVisibleNews] = useState(currentNews)
    const [newsLength, setNewsLength] = useState(0)

    function formatNews(news: News[], candidates: Candidate[]) {
        return news.map(n => {
            const candidate = candidates.find(c => c.id === n.id);
            return {
            ...n,
            name: candidate?.name, 
            };
        });
    }

    function updateCurrentNewsVisibility() {
        if (visibleNews < newsLength){
            const news = visibleNews + currentNews
            setVisibleNews(news)
        }
        
    }

    function previousPage() {
        if (visibleNews >= 0){
            const news = visibleNews - currentNews
            setVisibleNews(news)
        }
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
          const [candidatesRes, newsRes] = await Promise.all([
                fetch(`${apiUrl}/candidates`),
                fetch(`${apiUrl}/api/news`),
          ]);

          //feth candidates
          const data = await candidatesRes.json();
          const list = (data.candidates ?? []) as Candidate[];

          //fetch news
            const newsdata = await newsRes.json();
            const newslist = (newsdata ?? []) as News[];

            const newsformat = formatNews(newslist,list)
            setNewsLength(newslist.length)
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
        console.log(news)
  }, []);

   useEffect(() => {
    if (news) {
      console.log('Updated API data in state:', news); // Log after state update
    }
  }, [news]); // Run when apiData changes

    const [openIndex, setOpenIndex] = useState(-1)

    const toggle = (i: number) => {
    setOpenIndex(openIndex === i ? -1 : i);
  };

  return (
    <section className={s.pageBg}>
      <div className="container">
        {/* HERO / HEADER */}
        <div className={`hero ${s.heroSoft}`}>
          <div className="hero-body py-5">
            <div className={s.heroRow}>
              <div>
                <h1 className="title is-3 mb-1">Noticias Semanales</h1>
                <p className="subtitle is-6 has-text-grey">
                  Explora las noticias semanales de cada candidato
                </p>
              </div>
            </div>
          </div>
        </div>

        <ul className={s.grid} role="list">
          {news?.slice(visibleNews - currentNews, visibleNews).map((n, i) => (
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
        <div>
            {visibleNews > 3 && (
            <button onClick={previousPage}>Anterior</button>
        )}
          {visibleNews < news.length && (
        <button onClick={updateCurrentNewsVisibility}>Siguiente </button>
        )}
        </div>
        
      </div>
    </section>
  );
}