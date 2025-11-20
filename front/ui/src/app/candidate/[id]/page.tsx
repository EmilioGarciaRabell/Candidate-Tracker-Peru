"use client";
import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import { Candidate } from "@/interfaces/CandidateInterface";
import PublicOpinionSection from "./PublicOpinionSection";
import profilePicture from "./profile.jpg";
import styles from "./candidate.module.css";
import "bulma/css/bulma.min.css";

/* ===== Socials Types & Helpers (NEW) ===== */
type SocialsApi = {
  candidate_id: number;
  facebook?: string;
  instagram?: string;
  twitter?: string;
  youtube?: string;
  tiktok?: string;
  linkedin?: string;
  threads?: string;
  website?: string;
};

type SocialLink = { platform: string; url: string; handle?: string };

function ensureHttps(u = ""): string {
  return /^https?:\/\//i.test(u) ? u : u ? `https://${u}` : "";
}

function handleFromUrl(url: string): string | undefined {
  try {
    const u = new URL(url);
    const first = u.pathname.split("/").filter(Boolean)[0] || "";
    if (!first) return undefined;
    return first.startsWith("@") ? first : `@${first}`;
  } catch {
    return undefined;
  }
}

function normalizeToArray(obj: SocialsApi | null | undefined): SocialLink[] {
  if (!obj) return [];
  const known = [
    "twitter",
    "facebook",
    "instagram",
    "youtube",
    "tiktok",
    "linkedin",
    "threads",
    "website",
  ] as const;

  const out: SocialLink[] = [];
  for (const k of known) {
    const raw = (obj as any)[k];
    if (!raw) continue;
    const url = ensureHttps(String(raw));
    out.push({ platform: k, url, handle: handleFromUrl(url) });
  }
  return out;
}


function safeHostname(url: string) {
  try { return new URL(url).hostname; }
  catch { return url; }
}


/* ===== Page Component ===== */
export default function CandidatePage() {
  const params = useParams();
  const id = Array.isArray(params?.id) ? params.id[0] : (params?.id as string | undefined);

  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [loading, setLoading] = useState(true);
  const socialsFetchedRef = useRef(false)
  const [activeTab, setActiveTab] = useState<
    "historia" | "educacion" | "experienciaLaboral" | "polemicas" |  "propuestas" |"opinionPublica" | "redes" | "referencias" 
  >("historia");

  // socials state (NEW)
  const [socials, setSocials] = useState<SocialLink[]>([]);
  const [socialLoading, setSocialLoading] = useState(false);
  const [socialError, setSocialError] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageFailed, setImageFailed] = useState(false);
  const safeImageSrc = imageFailed || !imageUrl ? profilePicture.src : imageUrl;


  // Fetch Candidate (unchanged)
  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch(`${apiUrl}/candidate/${id}`, { cache: "no-store" });
        if (!res.ok) throw new Error("Fetch failed");
        const data = await res.json();
        if (!cancelled) setCandidate(data.candidate ?? null);
        
      } catch {
        if (!cancelled) setCandidate(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    
    return () => { cancelled = true; };
  }, [id, apiUrl]);

  useEffect(() => {
    const fetch_images = async () => {
      try {
        const res = await fetch(`${apiUrl}/image/${id}`, { cache: "no-store" });
        if (!res.ok) throw new Error("Failed image request");

        const data = await res.json();
        setImageUrl(data.url);
      } catch (e) {
        setImageFailed(true);
      }
  };

  fetch_images();
}, [id]);

  // Fetch Socials only when “redes” is opened first time (NEW)
 useEffect(() => {
  if (!id) return;
  if (socialsFetchedRef.current) return;

  socialsFetchedRef.current = true;

  setSocialLoading(true);
  setSocialError(null);

  let cancelled = false;

  (async () => {
    try {
      const res = await fetch(`${apiUrl}/candidate/social/${id}`, { cache: "no-store" });
      if (!res.ok) throw new Error(`Error ${res.status}`);

      const payload = await res.json();
      const arr = normalizeToArray(payload?.socials);

      if (!cancelled) setSocials(arr);

    } catch (err: any) {
      if (!cancelled) setSocialError(err.message);
    } finally {
      if (!cancelled) setSocialLoading(false);
    }
  })();

  return () => { cancelled = true; };
}, [id, apiUrl]);


  const tabs = [
    ["historia", "Historia"],
    ["educacion", "Educacion"],
    ["experienciaLaboral", "Experencia Laboral"],
    ["propuestas", "Propuestas"],
    ["polemicas", "Polemicas"],
    ["opinionPublica", "Opinión Pública"],
    // ["redes", "Redes Sociales"],
    ["referencias","Referencias"]
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
            <p className="has-text-grey">Verifica el enlace o intenta nuevamente más tarde.</p>
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
                <li><a href="/candidates">Candidatos</a></li>
                <li className="is-active"><a aria-current="page">Candidato</a></li>
              </ul>
            </nav>

            <h1 className="title is-3 mb-1">{candidate.name}</h1>
            <p className="subtitle is-6 has-text-grey-dark">
              {candidate.party_id ? (
                <span className={`tag is-info is-light ${styles.tagElevated}`}>Partido {candidate.party_id}</span>
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
              <div className="card-image">
                <figure className={`image is-square ${styles.imageWrapper}`}>
                  <img
                    src={safeImageSrc}
                    onError={() => setImageFailed(true)}
                    alt={`${name} profile image`}
                    className={styles.profileImage}
                    width={72}
                    height={72}
                  />
                </figure>
              </div>

              <div className="card-content">
                <p className="title is-6 mb-3">Redes Sociales</p>
                  <div className={styles.subtleDivider} />

                  {socialLoading && (
                    <ul className={styles.socialGrid} role="list" aria-busy="true">
                      {Array.from({ length: 6 }).map((_, i) => (
                        <li key={i} className={styles.socialSkeleton} />
                      ))}
                    </ul>
                  )}

                  {!socialLoading && socialError && (
                    <div className="notification is-danger is-light">
                      <p className="mb-2"><strong>Ocurrió un problema:</strong> {socialError}</p>
                      <button
                        className="button is-danger is-light is-small mt-2"
                        onClick={() => {
                          setSocials([]);
                          setSocialError(null);
                          setActiveTab("redes"); // retrigger fetch
                        }}
                      >
                        Reintentar
                      </button>
                    </div>
                  )}

                  {!socialLoading && !socialError && socials.length === 0 && (
                    <p className="has-text-grey">No hay redes sociales registradas.</p>
                  )}

                  {!socialLoading && !socialError && socials.length > 0 && (
                    <ul className={styles.socialGrid} role="list">
                      {socials.map((s, idx) => (
                        <li key={`${s.platform}-${idx}`}>
                          <a
                            className={styles.socialLink}
                            href={s.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            aria-label={`${s.platform} ${s.handle || ""}`.trim()}
                          >
                            <span className={styles.iconWrap} aria-hidden="true">
                              <PlatformIcon platform={s.platform} />
                            </span>
                            <span className={styles.socialText}>
                              <span className={styles.socialHandle}>
                                {s.handle || prettifyPlatform(s.platform)}
                              </span>
                              <span className={styles.socialUrl}>{safeHostname(s.url)}</span>
                            </span>
                          </a>
                        </li>
                      ))}
                    </ul>
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
                  <p className="content">{candidate.summary ?? "No hay información disponible."}</p>
                </>
              )}

              {activeTab === "educacion" && (
                <>
                  <h3 className="title is-5">Educacion</h3>
                <div className={styles.subtleDivider} />
                  <p className="has-text-grey">{candidate.education ?? "No hay informacion disponible"}</p>
                </>
              )}

              {activeTab === "experienciaLaboral" && (
                <>
                  <h3 className="title is-5">Experiencia Laboral</h3>
                <div className={styles.subtleDivider} />
                  <p className="has-text-grey">{candidate.work_experience ?? "No hay informacion disponible"}</p>
                </>
              )}

              {activeTab === "polemicas" && (
                <>
                  <h3 className="title is-5">Antecedentes</h3>
                  <div className={styles.subtleDivider} />
                  <p className="has-text-grey">{candidate.polemicas ?? "No hay informacion disponible"}</p>
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


              {activeTab === "referencias" && (
                <>
                  <h3 className="title is-5">Referencias</h3>
                  <div className={styles.subtleDivider} />

              {!candidate.ref || candidate.ref.length === 0 ? (
                <p className="has-text-grey">No hay referencias registradas.</p>
              ) : (
                <div className={styles.refsGrid}>
                  {candidate.ref?.map((ref, i) => (
                    <div key={i} className={styles.refCard}>
                      <blockquote className={styles.refQuote}>
                        “{ref.quote}”
                      </blockquote>

                      <a
                        className={styles.refLink}
                        href={ref.link}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Ver fuente →
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ===== Icons & Labels (same as before) ===== */
function PlatformIcon({ platform }: { platform: string }) {
  const p = platform.toLowerCase();
  const stroke = "currentColor";
  const common = { stroke, strokeWidth: 1.6, strokeLinecap: "round", strokeLinejoin: "round" } as const;

  if (p === "twitter" || p === "x") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path fill="currentColor" d="M13.7 10.3 20.8 3h-1.7l-6.2 6.7L8.2 3H3.1l7.5 10.9L3.1 21h1.7l6.6-7.1 5 7.1h5.1l-7.8-10.7Z"/>
      </svg>
    );
  }
  if (p === "facebook") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path fill="currentColor" d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.3v3.2h2.8V22h3.4z"/>
      </svg>
    );
  }
  if (p === "instagram") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke={stroke} strokeWidth="1.6" />
        <circle cx="12" cy="12" r="3.5" fill="none" stroke={stroke} strokeWidth="1.6" />
        <circle cx="17.2" cy="6.8" r="1" fill="currentColor" />
      </svg>
    );
  }
  if (p === "youtube") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path fill="currentColor" d="M22 12s0-3.4-.4-5c-.2-.8-.9-1.5-1.7-1.7C18.3 5 12 5 12 5s-6.3 0-7.9.3c-.8.2-1.5.9-1.7 1.7C2 8.6 2 12 2 12s0 3.4.4 5c.2.8.9 1.5 1.7 1.7C5.7 19 12 19 12 19s6.3 0 7.9-.3c.8-.2 1.5-.9 1.7-1.7.4-1.6.4-5 .4-5Zm-12 3.1V8.9L15.5 12 10 15.1Z"/>
      </svg>
    );
  }
  if (p === "tiktok") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path fill="currentColor" d="M19 7.6c-2 0-3.8-1.1-4.7-2.7v7.6c0 3.2-2.6 5.7-5.7 5.7S3 15.7 3 12.6 5.6 6.9 8.7 6.9c.5 0 1 .1 1.5.2v3.1c-.5-.2-1-.3-1.5-.3-1.7 0-3.1 1.4-3.1 3.1S7 16.1 8.7 16.1s3.1-1.4 3.1-3.1V2.9h3.4c.5 2.2 2.4 3.9 4.7 4.1V7.6Z"/>
      </svg>
    );
  }
  if (p === "linkedin") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path fill="currentColor" d="M4.98 3.5C4.98 4.88 3.86 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V23h-4V8zm7.5 0h3.8v2.1h.1c.5-1 1.9-2.1 4-2.1 4.3 0 5.1 2.8 5.1 6.5V23h-4v-6.5c0-1.6 0-3.8-2.3-3.8s-2.6 1.8-2.6 3.6V23h-4V8z"/>
      </svg>
    );
  }
  if (p === "threads") {
    return (
      <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path fill="currentColor" d="M12 2c5.5 0 10 4.5 10 10s-4.5 10-10 10S2 17.5 2 12 6.5 2 12 2Zm3.4 12.6c-.5 2-2.2 3.3-4.4 3.3-2.5 0-4.3-1.8-4.3-4.3 0-2.6 1.9-4.5 4.6-4.5 1.7 0 3.2.8 4 2.1l-1.3.8c-.5-.8-1.4-1.3-2.6-1.3-1.8 0-3 .9-3.2 2.6h7.1c.1.5.1 1 0 1.3Zm-7.1-.7c.2 1.4 1.3 2.3 2.7 2.3 1.3 0 2.4-.8 2.6-2.3H8.3Z"/>
      </svg>
    );
  }
  // generic
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
      <circle cx="12" cy="12" r="9" fill="none" {...common} />
      <path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18" fill="none" {...common} />
    </svg>
  );
}

function prettifyPlatform(p: string) {
  const m: Record<string, string> = {
    twitter: "Twitter",
    facebook: "Facebook",
    instagram: "Instagram",
    youtube: "YouTube",
    tiktok: "TikTok",
    linkedin: "LinkedIn",
    threads: "Threads",
    website: "Sitio web",
  };
  return m[p.toLowerCase()] ?? p;
}
