"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Image from "next/image";
import { Candidate } from "@/interfaces/CandidateInterface";
import PublicOpinionSection from "./PublicOpinionSection";
import profilePicture from "./profile.jpg";
import styles from "./candidate.module.css";
import "bulma/css/bulma.min.css";

export default function CandidatePage() {
  const params = useParams();
  const id = Array.isArray(params?.id) ? params.id[0] : (params?.id as string | undefined);

  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<
    "historia" | "antecedentes" | "opinionPublica" | "propuestas" | "redes"
  >("historia");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    (async () => {
      try {
        const res = await fetch(`${apiUrl}/candidate/${id}`);
        if (!res.ok) throw new Error("Fetch failed");
        const data = await res.json();
        if (!cancelled) setCandidate(data.candidate ?? null);
      } catch {
        if (!cancelled) setCandidate(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [id, apiUrl]);

  const tabs = [
    ["historia", "Historia"],
    ["antecedentes", "Antecedentes"],
    ["opinionPublica", "Opinión Pública"],
    ["propuestas", "Propuestas"],
    ["redes", "Redes Sociales"],
  ] as const;

  if (loading) {
    return (
      <section className={`section ${styles.pageBg}`}>
        <div className="container">
          <div className={`${styles.skeletonHero} mb-5`} />
          <div className="columns is-variable is-6">
            <aside className="column is-12-mobile is-4-tablet is-3-desktop">
              <div className={`${styles.cardSoft} ${styles.skeletonBlock}`} />
            </aside>
            <div className="column">
              <div className={`${styles.boxSoft} ${styles.skeletonBlock} mb-4`} />
              <div className={`${styles.boxSoft} ${styles.skeletonBlock}`} />
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (!candidate) {
    return (
      <section className={`section ${styles.pageBg}`}>
        <div className="container has-text-centered">
          <div className="box is-inline-block">
            <p className="title is-4 mb-2">Candidate not found</p>
            <p className="has-text-grey">
              Verifica el enlace o intenta nuevamente más tarde.
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className={`section ${styles.pageBg}`}>
      <div className="container">
        {/* HEADER / HERO */}
        <div className={`hero ${styles.heroSoft}`}>
          <div className="hero-body py-5">
            <nav className="breadcrumb is-small mb-2" aria-label="breadcrumbs">
              <ul>
                <li><a href="/">Inicio</a></li>
                <li className="is-active"><a aria-current="page">Candidato</a></li>
              </ul>
            </nav>

            <h1 className="title is-3 mb-1">{candidate.name}</h1>
            <p className="subtitle is-6 has-text-grey-dark">
              {candidate.party_id ? (
                <>
                  <span className={`tag is-info is-light ${styles.tagElevated}`}>
                    Partido {candidate.party_id}
                  </span>
                </>
              ) : (
                <span className={`tag is-light ${styles.tagElevated}`}>Sin partido asignado</span>
              )}
            </p>
          </div>
        </div>

        <div className="columns is-variable is-6 mt-5">
          {/* LEFT SIDEBAR */}
          <aside className="column is-12-mobile is-4-tablet is-3-desktop">
            <div className={`${styles.cardSoft} card ${styles.stickyAside}`}>
              {/* Photo */}
              <div className="card-image">
                <figure className={`image is-square ${styles.imageWrapper}`}>
                  <Image
                    src={profilePicture}
                    alt={candidate.name}
                    width={500}
                    height={500}
                    className={styles.profileImage}
                    priority
                  />
                </figure>
              </div>

              {/* Experience */}
              <div className="card-content">
                <p className="title is-6 mb-3">Experiencia Laboral</p>
                {candidate.summary ? (
                  <p className="is-size-7 has-text-grey">{candidate.summary}</p>
                ) : (
                  <p className="is-size-7 has-text-grey-light">
                    No se ha proporcionado experiencia laboral.
                  </p>
                )}
              </div>
            </div>
          </aside>

          {/* MAIN CONTENT */}
          <div className="column">
            {/* TABS */}
            <nav className={styles.navBar} role="tablist">
              {tabs.map(([key, label]) => {
                const isActive = activeTab === key;
                return (
                  <button
                    key={key}
                    className={`${styles.navItem} ${isActive ? styles.active : ""}`}
                    onClick={() => setActiveTab(key as typeof activeTab)}
                    aria-selected={isActive}
                    aria-controls={`panel-${key}`}
                  >
                    {label}
                  </button>
                );
              })}
            </nav>


            {/* CONTENT BOX */}
            <div className={`box ${styles.boxSoft}`} id={`panel-${activeTab}`} role="tabpanel">
              {activeTab === "historia" && (
                <>
                  <h3 className="title is-5">Acerca de mí</h3>
                  <p className="content">
                    {candidate.summary ?? "No hay información disponible."}
                  </p>
                </>
              )}

              {activeTab === "antecedentes" && (
                <>
                  <h3 className="title is-5">Antecedentes</h3>
                  <div className={styles.subtleDivider} />
                  <p className="has-text-grey">
                    No hay antecedentes registrados.
                  </p>
                </>
              )}

              {activeTab === "opinionPublica" && (
                <>
                  <h3 className="title is-5">Opinión Pública</h3>
                  <div className={styles.subtleDivider} />
                  <PublicOpinionSection candidateId={candidate.id} />
                </>
              )}

              {activeTab === "propuestas" && (
                <>
                  <h3 className="title is-5">Propuestas</h3>
                  <div className={styles.subtleDivider} />
                  <p className="has-text-grey">No se han registrado propuestas.</p>
                </>
              )}

              {activeTab === "redes" && (
                <>
                  <h3 className="title is-5">Redes Sociales</h3>
                  <div className={styles.subtleDivider} />
                  <p className="has-text-grey">No hay redes sociales registradas.</p>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
