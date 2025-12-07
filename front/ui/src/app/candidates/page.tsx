"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import UserCard from "@/components/UserCard";
import { Candidate } from "@/interfaces/CandidateInterface";
import s from "./candidates.module.css";
import "bulma/css/bulma.min.css";

export default function Candidates() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortOption, setSortOption] = useState("");

  const [query, setQuery] = useState("");
  const [partyFilter, setPartyFilter] = useState<string>("");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

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
      const shuffled = shuffleArray<Candidate>(data.candidates ?? []);
      setCandidates(shuffled);
    } catch (err: any) {
      setError(err?.message || "Error al cargar candidatos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const parties = useMemo(() => {
    const set = new Set<string>();
    candidates.forEach((c) => {
      if (c.party_id) set.add(String(c.party_id));
    });
    return Array.from(set).sort();
  }, [candidates]);


  const filtered = useMemo(() => {
  const q = query.trim().toLowerCase();

  let result = candidates.filter((c) => {
    const nameAndNicknames = [
      c.name?.toLowerCase(),
      ...(c.nicknames?.map((n) => n.toLowerCase()) ?? []),
    ];

    const matchesQuery =
      !q ||
      nameAndNicknames.some((field) => field?.includes(q)) ||
      c.summary?.toLowerCase().includes(q);

    const matchesParty =
      !partyFilter || String(c.party_id) === partyFilter;

    return matchesQuery && matchesParty;
  });

  if (sortOption === "name-asc") {
    result = [...result].sort((a, b) =>
      a.name.localeCompare(b.name)
    );
  } else if (sortOption === "name-desc") {
    result = [...result].sort((a, b) =>
      b.name.localeCompare(a.name)
    );
  } else if (sortOption === "age-asc") {
    result = [...result].sort((a, b) => (a.age ?? 0) - (b.age ?? 0));
  } else if (sortOption === "age-desc") {
    result = [...result].sort((a, b) => (b.age ?? 0) - (a.age ?? 0));
  }

  return result;
}, [candidates, query, partyFilter, sortOption]);




  function shuffleArray<T>(array: T[]): T[] {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // Loading (ONLY DATA)
  if (loading) {
    return (
      <section className={`section ${s.pageBg}`}>
        <div className="container">
          <div className={`hero ${s.heroSoft}`}>
            <div className="hero-body py-5">
              <h1 className="title is-4 mb-1">Candidatos</h1>
              <p className="subtitle is-6 has-text-grey">
                Cargando información…
              </p>
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

  // Error
  if (error) {
    return (
      <section className="section">
        <div className="container">
          <div className="notification is-danger is-light">
            <p className="mb-3">
              <strong>Ocurrió un problema</strong>
            </p>
            <p className="mb-4">{error}</p>
            <button className="button is-danger is-light" onClick={fetchCandidates}>
              Reintentar
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className={`section ${s.pageBg}`}>
      <div className="container">
        <div className={`hero ${s.heroSoft}`}>
          <div className="hero-body py-5">
            <div className={s.heroRow}>
              <div>
                <h1 className="title is-3 mb-1">Candidatos</h1>
                <p className="subtitle is-6 has-text-grey">
                  Explora y filtra por nombre o partido.
                </p>
              </div>
              <span className={`tag is-light ${s.countTag}`}>
                {filtered.length} de {candidates.length}
              </span>
            </div>
          </div>
        </div>

        {/* FILTER BAR (module.css based) */}
<div className={`box ${s.filtersBox} mt-5`}>
  <div className={s.filterBar}>

    {/* Search Input */}
    <div className={s.filterGroup + " " + s.grow}>
      <label className={s.label}>Buscar</label>
      <div className={s.control}>
        <input
          className={`${s.input} ${s.inputWithIcon}`}
          type="text"
          placeholder="Nombre, apodo o partido…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <span className={s.iconLeft}>
          <i className="fas fa-search" />
        </span>
      </div>
    </div>

    {/* Party Filter (NOT REMOVED) */}
    <div className={s.filterGroup}>
      <label className={s.label}>Partido</label>
      <div className={s.control}>
        <div className={s.selectWrap}>
          <select
            value={partyFilter}
            onChange={(e) => setPartyFilter(e.target.value)}
            className={s.select}
          >
            <option value="">Todos los partidos</option>
            {parties.map((p) => (
              <option key={p} value={p}>
                Partido {p}
              </option>
            ))}
          </select>
          <span className={s.selectArrow}>▼</span>
        </div>
      </div>
    </div>

    {/* Sort Filter */}
    <div className={s.filterGroup}>
      <label className={s.label}>Ordenar por</label>
      <div className={s.control}>
        <div className={s.selectWrap}>
          <select
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value)}
            className={s.select}
          >
            <option value="">Sin ordenar</option>
            <option value="name-asc">Nombre (A-Z)</option>
            <option value="name-desc">Nombre (Z-A)</option>
            <option value="age-asc">Edad (menor → mayor)</option>
            <option value="age-desc">Edad (mayor → menor)</option>
          </select>
          <span className={s.selectArrow}>▼</span>
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
              Intenta limpiar los filtros o usa otro término.
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
  );
}
