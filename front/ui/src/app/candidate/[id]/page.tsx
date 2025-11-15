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
  const id = Array.isArray(params?.id) ? params.id[0] : params?.id;
  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<
    "historia" | "antecedentes" | "opinionPublica" | "propuestas" | "redes"
  >("historia");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  // Fetch Candidate
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

  if (loading) return <p className="has-text-centered mt-6">Loading...</p>;
  if (!candidate) return <p className="has-text-centered mt-6">Candidate not found</p>;

  const tabs = [
    ["historia", "Historia"],
    ["antecedentes", "Antecedentes"],
    ["opinionPublica", "Opinión Pública"],
    ["propuestas", "Propuestas"],
    ["redes", "Redes Sociales"],
  ] as const;

  return (
    <section className="section has-background-white-ter">
      <div className="container">

        <div className="columns is-variable is-6">

          {/* LEFT SIDEBAR */}
          <aside className="column is-one-quarter">

            <div className="card" style={{ borderRadius: 12 }}>
              {/* Photo */}
              <div className="card-image">
                <figure className={`image is-square ${styles.imageWrapper}`}>
                  <Image
                    src={profilePicture}
                    alt={candidate.name}
                    width={500}
                    height={500}
                    className={styles.profileImage}
                  />
                </figure>
              </div>

              {/* Experience */}
              <div className="card-content">
                <p className="title is-5 mb-3">Experiencia Laboral</p>

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

            {/* Candidate Name */}
            <h2 className="title is-3 mb-1">{candidate.name}</h2>
            <p className="subtitle is-6 has-text-grey-dark mb-4">
              {candidate.party_id
                ? `Partido ${candidate.party_id}`
                : "Sin partido asignado"}
            </p>

            {/* TABS */}
            <div className={`tabs ${styles.cleanTabs}`}>


              <ul>
                {tabs.map(([key, label]) => (
                  <li key={key} className={activeTab === key ? "is-active" : ""}>
                    <a onClick={() => setActiveTab(key as any)}>
                      <span>{label}</span>
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* MAIN CONTENT BOX */}
            <div className="box has-background-white" style={{ borderRadius: 10 }}>

              {activeTab === "historia" && (
                <>
                  <h3 className="title is-5">Acerca de mí</h3>
                  <p>{candidate.summary ?? "No hay información disponible."}</p>
                </>
              )}

              {activeTab === "antecedentes" && (
                <>
                  <h3 className="title is-5">Antecedentes</h3>
                  <p>No hay antecedentes registrados.</p>
                </>
              )}

              {activeTab === "opinionPublica" && (
                <PublicOpinionSection candidateId={candidate.id} />
              )}

              {activeTab === "propuestas" && (
                <>
                  <h3 className="title is-5">Propuestas</h3>
                  <p>No se han registrado propuestas.</p>
                </>
              )}

              {activeTab === "redes" && (
                <>
                  <h3 className="title is-5">Redes Sociales</h3>
                  <p>No hay redes sociales registradas.</p>
                </>
              )}

            </div>

          </div>
        </div>

      </div>
    </section>
  );
}
