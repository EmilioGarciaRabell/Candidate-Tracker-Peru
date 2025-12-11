"use client";

import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import { Party } from "@/interfaces/Party";
import profilePicture from "./profile.jpg";
import styles from "./partido.module.css";

import "bulma/css/bulma.min.css";

export default function PartidoPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  const params = useParams();
  const id = Array.isArray(params?.id)
    ? params.id[0]
    : (params?.id as string | undefined);

  const [party, setParty] = useState<Party | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<
    "ideologia" | "historia" | "referencias"
  >("historia");

  // Image state
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageFailed, setImageFailed] = useState(false);
  const safeImageSrc =
    imageFailed || !imageUrl ? profilePicture.src : imageUrl;

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }
    let cancelled = false;

    (async () => {
      try {
        const res = await fetch(`${apiUrl}/party/${id}`, { cache: "no-store" });
        if (!res.ok) throw new Error("Fetch failed");
        const data = await res.json();
        if (!cancelled) setParty(data.party ?? null);
      } catch {
        if (!cancelled) setParty(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [id, apiUrl]);

  useEffect(() => {
    const fetch_images = async () => {
      try {
        const res = await fetch(`${apiUrl}/pImage/${id}`, { cache: "no-store" });
        if (!res.ok) throw new Error("Failed image request");
        const data = await res.json();
        setImageUrl(data.url);
      } catch (e) {
        setImageFailed(true);
      }
    };

    fetch_images();
  }, [id]);

  const tabs = [
    ["historia", "Historia"],
    ["ideologia", "Ideologia"],
    ["referencias", "Referencias"]
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

  if (!party) {
    return (
      <section className={`section ${styles.pageBg}`}>
        <div className="container has-text-centered">
          <div className="box is-inline-block">
            <p className="title is-4 mb-2">Party not found</p>
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
                <li><a href="/parties">Partidos</a></li>
                <li className="is-active"><a aria-current="page">Partido</a></li>
              </ul>
            </nav>
            <h1 className="title is-3 mb-1">{party.name}</h1>
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
                    alt={`${party.name} profile image`}
                    className={styles.profileImage}
                    width={72}
                    height={72}
                  />
                </figure>
              </div>
              <div className="card-content">
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
                  <h3 className="title is-5">Historia</h3>
                  <p className="content">{party.summary ?? "No hay información disponible."}</p>
                </>
              )}
              {activeTab === "ideologia" && (
                <>
                  <h3 className="title is-5">Ideologia</h3>
                  <div className={styles.subtleDivider} />
                  <p className="has-text-grey">{party.position}</p>
                </>
              )}
              {activeTab === "referencias" && (
                <>
                  <h3 className="title is-5">Referencias</h3>
                  <div className={styles.subtleDivider} />
                  {party.ref.map((item, index) => (
                    <ul key={`${item}-${index}`}>
                      <li> <a>{item}</a></li>
                    </ul>
                   
                  ))}
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
