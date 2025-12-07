"use client";

import { useEffect, useState, useMemo } from "react"
import "bulma/css/bulma.min.css";
import { Candidate } from "@/interfaces/CandidateInterface";
import { News } from "@/interfaces/News";
import s from "./noticias.module.css";



export default function Noticias(){
    const [news, setNews] = useState<News[]>([])

    const apiUrl = process.env.NEXT_PUBLIC_API_URL;

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const currentNews = 3
    const [currentPage, setCurrentPage] = useState(0)
    const [filteredNews, setFilteredNews] = useState<News[]>([])
    

    function formatNews(news: News[], candidates: Candidate[]) {
        return news.map(n => {
            const candidate = candidates.find(c => c.id === n.candidate_id);
            return {
            ...n,
            name: candidate?.name.normalize('NFD').replace(/[\u0300-\u036f]/g, ''), 
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
    }, []);

    const [openIndex, setOpenIndex] = useState(-1)

    const toggle = (i: number) => {
    setOpenIndex(openIndex === i ? -1 : i);
  };

   const [query, setQuery] = useState("");


    const totalPages = Math.ceil(filteredNews.length / currentNews)
    const start = currentPage * currentNews
    const end = start + currentNews
    const visibleNews = filteredNews.slice(start, end)
    console.log(visibleNews)

    useEffect(() => {
        setOpenIndex(-1);
    }, [currentPage]);

    const nextPage = () => {
        if (currentPage < totalPages - 1) {
        setCurrentPage(currentPage + 1)
        
        }
    }

    const previousPage = () => {
        if (currentPage > 0) {
        setCurrentPage(currentPage - 1)
        console.log("noticias")
        console.log(visibleNews)
        }
    }

   useEffect(() => {
        const q = query.toLowerCase()
        const f = news.filter((c)=>{
            return c.name?.toLowerCase().includes(q)
        })
        setFilteredNews(f)
        setCurrentPage(0);

    }, [news,query]);



   if (loading) {
    return (
      <section className={`section ${s.pageBg}`}>
        <div className="container">
          <div className={`hero ${s.heroSoft}`}>
            <div className="hero-body py-5">
              <h1 className="title is-4 mb-1">Noticias</h1>
              <p className="subtitle is-6 has-text-grey">Cargando información…</p>
            </div>
          </div>

          <div className={`mt-5 ${s.grid}`}>
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className={s.skeletonCard} />
            ))}
          </div>
        </div>
      </section>
    );
  }

  // Error state
  if (error) {
    return (
      <section className="section">
        <div className="container">
          <div className="notification is-danger is-light">
            <p className="mb-3"><strong>Ocurrió un problema</strong></p>
            <p className="mb-4">{error}</p>
            <button className="button is-danger is-light">
              Reintentar
            </button>
          </div>
        </div>
      </section>
    );
  } 
  return (
    <section className={s.pageBg}>
      <div className="container gap-5">
        {/* HERO / HEADER */}
        <div className={`hero ${s.heroSoft}`}>
          <div className="hero-body py-5">
            <div className={s.heroRow}>
              <div>
                <h1 className="title is-3 mb-1">Noticias Semanales</h1>
                <p className="subtitle is-6 has-text-grey mt-2">
                  Explora las noticias semanales de cada candidato
                </p>
              </div>
            </div>
          </div>
        </div>
        {/* CONTROLS */}

        <div className={`box ${s.filtersBox} mt-5`}>
                  <div className="columns is-variable is-4 is-multiline">
                    <div className="column is-12-mobile is-7-tablet">
                      <div className="field">
                        <div className="control has-icons-left">
                          <input
                            className={`input ${s.input}`}
                            type="text"
                            placeholder="Buscar por nombre"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            aria-label="Buscar"
                          />
                          <span className="icon is-small is-left">
                            <i className="fas fa-search" aria-hidden="true"></i>
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
        </div>
         {/* GRID */}
        {visibleNews.length === 0 ? (
          <div className="box has-text-centered">
            <p className="title is-5 mb-2">No se encontraron noticias del candidato</p>
            <p className="has-text-grey mb-4">
              Intenta limpiar los filtros o utiliza otro término de búsqueda.
            </p>
            <button
              className="button is-light"
              onClick={() => {
                setQuery("");
              }}
            >
              Limpiar filtros
            </button>
          </div>
        ) : (
        <ul className={s.grid} role="list">
          {visibleNews.map((n, i) => (
            <li key={n.candidate_id} className={s.gridItem} role="listitem">
              <div className={s.dropdown}>
                <button
                  className={s.dropdownHeader}
                  onClick={() => toggle(i)}
                >
                
                <span className={s.name}>{n.name} </span>
                <span></span>
                
                <div className={s.extraItems}>
                  
                  <span
                    className={`${s.caret} ${
                      openIndex === i ? s.open : ""
                    }`}
                  >
                    +
                  </span>
                </div>
                 
                </button>

                <div
                  className={`${s.dropdownBody} ${
                    openIndex === i ? s.show : ""
                  }`}
                >
                    <div className={s.scroll}>
                    {n.news_json?.map((item, j) => (
                    <a key={j} href={item.link} className={s.dropdownItem}>
                      {item.title}
                    </a>
                  ))}
                    </div>
                 
                </div>
              </div>
            </li>
          ))}
        </ul>)}

        {/* BUTTONS */}
        <div className={s.buttons}>
           
                    <button
                    className={s.linkButton}
                    onClick={previousPage}
                    disabled={currentPage === 0}
                    >
                &larr; Anterior
                </button>
        
         
                <button
                    className={s.linkButton}
                    onClick={nextPage}
                    disabled={currentPage >= totalPages - 1}
                    >
                Siguiente &rarr;
                </button>
        </div>
      </div>
    </section>
  );
}