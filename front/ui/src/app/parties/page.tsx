"use client";

import { useEffect, useMemo, useState } from "react";
import UserCard from "@/components/partidoCard";
import s from "../candidates/candidates.module.css";
import "bulma/css/bulma.min.css";
import { Party } from "@/interfaces/Party";

export default function parties(){
    const [parties,setParties] = useState<Party[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

// UI controls
    const [query, setQuery] = useState("");
    const [partyFilter, setPartyFilter] = useState<string>("");

    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    async function getParties(){
        setLoading(true);
        setError(null);
        try{
            const res = await fetch(`${apiUrl}/parties`, { cache: "no-store" });
            if (!res.ok) throw new Error(`Error ${res.status}`);
            const data = await res.json();
            setParties(data.parties ?? []);

        }catch(err:any){
            setError(err?.message || "Error al cargar candidatos");
        }finally{
             setLoading(false);
        }
    }
    useEffect(() => {
        getParties()
    },[])

    const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return parties.filter((c) => {
      const matchesQuery =
        !q ||
        c.name?.toLowerCase().includes(q) ||
        c.summary?.toLowerCase().includes(q);
    //   const matchesParty = !partyFilter || String(c.party_id) === partyFilter;
      return matchesQuery 
    });
  }, [parties, query]);


    // Loading skeleton
  if (loading) {
    return (
      <section className={`section ${s.pageBg}`}>
        <div className="container">
          <div className={`hero ${s.heroSoft}`}>
            <div className="hero-body py-5">
              <h1 className="title is-4 mb-1">Candidatos</h1>
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
            <button className="button is-danger is-light" onClick={getParties}>
              Reintentar
            </button>
          </div>
        </div>
      </section>
    );
  }

    return <section className={`section ${s.pageBg}`}>
        <div className="container">
            {/* HERO / HEADER */}
        <div className={`hero ${s.heroSoft}`}>
          <div className="hero-body py-5">
            <div className={s.heroRow}>
              <div>
                <h1 className="title is-3 mb-1">Partidos</h1>
                <p className="subtitle is-6 has-text-grey">Explora y filtra por nombre</p>
              </div>
              <span className={`tag is-light ${s.countTag}`}>
                {partyFilter.length} de {parties.length}
              </span>
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
                    placeholder="Buscar por nombre o descripción…"
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

            <div className="column is-12-mobile is-5-tablet">
              <div className="field">
                <div className="control">
                  <div className={`select is-fullwidth ${s.select}`}>
                    <select
                      value={partyFilter}
                      onChange={(e) => setPartyFilter(e.target.value)}
                      aria-label="Filtrar por partido"
                    >
                      <option value="">Todos los partidos</option>
                      {parties.map((p) => (
                        <option key={p.id} value={p.id}>
                          Partido {p.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* GRID */}
        {filtered.length === 0 ? (
          <div className="box has-text-centered">
            <p className="title is-5 mb-2">No se encontraron candidatos</p>
            <p className="has-text-grey mb-4">
              Intenta limpiar los filtros o utiliza otro término de búsqueda.
            </p>
            <button
              className="button is-light"
              onClick={() => {
                setQuery("");
                setPartyFilter("");
              }}
            >
              Limpiar filtros
            </button>
          </div>
        ) : (
          <ul className={s.grid} role="list">
            {filtered.map((c) => (
              <li key={c.id} className={s.gridItem} role="listitem">
                <UserCard {...c} />
              </li>
            ))}
          </ul>
        )}
        </div>
    </section>
    
}