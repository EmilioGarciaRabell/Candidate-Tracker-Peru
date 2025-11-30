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

  // UI controls
  const [query, setQuery] = useState("");
  const [partyFilter, setPartyFilter] = useState<string>("");

  // image loading tracking
  const [imagesDone, setImagesDone] = useState(0);
  const [allImagesReady, setAllImagesReady] = useState(false);

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
      const list = (data.candidates ?? []) as Candidate[];
      const shuffled = shuffleArray<Candidate>(list);

      setCandidates(shuffled);
    } catch (err: any) {
      setError(err?.message || "Error al cargar candidatos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const parties = useMemo(() => {
    const set = new Set<string>();
    candidates.forEach((c) => {
      if (c.party_id) set.add(String(c.party_id));
    });
    return Array.from(set).sort();
  }, [candidates]);

  // same filtered logic you already had
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return candidates.filter((c) => {
      const matchesQuery =
        !q ||
        c.name?.toLowerCase().includes(q) ||
        c.summary?.toLowerCase().includes(q);
      const matchesParty = !partyFilter || String(c.party_id) === partyFilter;
      return matchesQuery && matchesParty;
    });
  }, [candidates, query, partyFilter]);

  // whenever the list of cards changes, reset image counters
  useEffect(() => {
    if (filtered.length === 0) {
      setImagesDone(0);
      setAllImagesReady(true); // nothing to load
    } else {
      setImagesDone(0);
      setAllImagesReady(false);
    }
  }, [filtered]);

  // callback passed to each UserCard
  const handleImageReady = useCallback(() => {
    setImagesDone((prev) => {
      const next = prev + 1;
      if (next >= filtered.length) {
        setAllImagesReady(true);
      }
      return next;
    });
  }, [filtered.length]);


  function shuffleArray<T>(array: T[]): T[] {
  const arr = [...array]; // avoid mutating original
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

  // Loading skeleton (data)
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

  // Error state
  if (error) {
    return (
      <section className="section">
        <div className="container">
          <div className="notification is-danger is-light">
            <p className="mb-3">
              <strong>Ocurrió un problema</strong>
            </p>
            <p className="mb-4">{error}</p>
            <button
              className="button is-danger is-light"
              onClick={fetchCandidates}
            >
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
        {/* HERO / HEADER */}
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
                        <option key={p} value={p}>
                          Partido {p}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* IMAGE LOADING OVERLAY (only after data is ready) */}
        {!allImagesReady && filtered.length > 0 && (
          <div className={s.imageLoadingOverlay}>
            <div className={s.imageLoadingBox}>
              <p className="title is-5 mb-1">Cargando imágenes…</p>
              <p className="has-text-grey is-size-7">
                {imagesDone} / {filtered.length}
              </p>
            </div>
          </div>
        )}

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
                <UserCard {...c} onImageReady={handleImageReady} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
