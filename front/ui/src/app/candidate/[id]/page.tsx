"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Candidate } from "@/interfaces/CandidateInterface";
import Image from "next/image";
import s from "./candidate.module.css";
import profilePicture from "./profile.jpg";

export default function CandidatePage() {
  const { id } = useParams();
  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("historia"); 
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    if (!id) return;
    fetch(`${apiUrl}/candidate/${id}`)
      .then((res) => res.json())
      .then((data) => setCandidate(data.candidate)) 
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (!candidate) return <p>Candidate not found</p>;

  console.log(candidate.party_id)
  return (
    <div>
      <main className={s.profile_container}>
        {/* Left column */}
        <aside className={s.profile_sidebar}>
          <div className={s.profile_pic}>
            <Image  
              src={profilePicture}
              alt={candidate.name}
              width={900}
              height={900}
              style={{ borderRadius: "5%" }}
            />
          </div>

          <div className={s.work_section}>
            <h3>Experiencia Laboral</h3>
          
            {/* {candidate.experience ? (
              <ul className={s.experience_list}>
                {candidate.experience.map((exp, i) => (
                  <li key={i}>
                    <strong>{exp.title}</strong>
                    <p>{exp.description}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No se ha proporcionado experiencia laboral.</p>
            )} */}
          </div>
        </aside>

        {/* Right column */}
        <section className={s.profile_details}>
          <h2>{candidate.name}</h2>
          <p className={s.job_title}>
            {candidate.party_id ? `Partido ${candidate.party_id}` : "Sin partido asignado"}
          </p>
          <hr />

          {/* Tabs */}
          <nav className={s.nav_bar}>
            {["historia", "antecedentes", "opinionPublica", "propuestas", "redes"].map((tab) => (
              <button
                key={tab}
                className={`${s.nav_item} ${activeTab === tab ? s.active : ""}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>

          {/* Dynamic tab content */}
          <div className={s.tab_content}>
            {activeTab === "historia" && (
              <div className={s.social_section}>
                <h3>Acerca de mí</h3>
                <p>{candidate.summary || "No hay información disponible."}</p>
              </div>
            )}

            {activeTab === "antecedentes" && (
              <div className={s.antecedentes_section}>
                <h3>Antecedentes</h3>
                {/* {candidate.background ? (
                  candidate.background.map((item, i) => (
                    <div key={i} className={s.antecedente_item}>
                      <h4>{item.title}</h4>
                      <p>{item.description}</p>
                      {item.source && (
                        <a href={item.source} target="_blank" rel="noopener noreferrer">
                          Ver fuente
                        </a>
                      )}
                    </div>
                  ))
                ) : (
                  <p>No hay antecedentes registrados.</p>
                )} */}
              </div>
            )}

            {activeTab === "opinionPublica" && (
              <div className={s.public_opinion_section}>
                <h3>Opinión Pública</h3>
                <p>Datos extraídos del análisis de redes sociales y encuestas.</p>
              </div>
            )}

            {activeTab === "propuestas" && (
              <div className={s.antecedentes_section}>
                <h3>Propuestas</h3>
                {/* {candidate.proposals ? (
                  candidate.proposals.map((p, i) => (
                    <div key={i} className={s.antecedente_item}>
                      <h4>{p.title}</h4>
                      <p>{p.description}</p>
                    </div>
                  ))
                ) : (
                  <p>No se han registrado propuestas.</p>
                )} */}
              </div>
            )}

            {activeTab === "redes" && (
              <div className={s.social_section}>
                <h3>Redes Sociales</h3>
                {/* {candidate.socials ? (
                  <div className={s.social_links}>
                    {Object.entries(candidate.socials).map(([network, url]) => (
                      <a
                        key={network}
                        href={url as string}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <img src={`/icons/${network}.svg`} alt={network} />
                        <span>{network}</span>
                      </a>
                    ))}
                  </div>
                ) : (
                  <p>No hay redes sociales registradas.</p>
                )} */}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
