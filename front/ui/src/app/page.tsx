"use client";

import Image from "next/image";
import Link from "next/link";
import styles from "./home.module.css";

export default function Home() {
  return (
    <>
    
      <section
        aria-labelledby="home-title"
        className={styles.background}
        role="region"
      >
        <div className={styles.shell}>
          <div className={styles.hero}>
            {/* Copy */}
            <header className={styles.copy}>
              <p className={styles.kicker}>
                Por un Perú informado rumbo a las elecciones 2026
              </p>

              <h1 id="home-title" className={styles.title}>
                Infórmate por un <span className={styles.titleAccent}>Perú mejor</span>
              </h1>

              <p className={styles.subtitle}>
                Descubre candidatos, propuestas y opinión pública en un sólo lugar.
                Datos claros, diseño ligero y accesible — para decidir mejor.
              </p>

              <div className={styles.ctaRow} id="main">
                <Link href="/candidates" className={styles.ctaPrimary} aria-label="Ir a lista de candidatos">
                  Infórmate ahora
                </Link>
                
              </div>

              {/* Tiny trust row */}
              <ul className={styles.badges} role="list" aria-label="Aspectos destacados">
                <li className={styles.badge}>Actualizado</li>
                <li className={styles.badge}>Transparente</li>
                <li className={styles.badge}>Accesible</li>
              </ul>
            </header>

            {/* Illustration */}
            <div className={styles.imageWrap} aria-hidden="true">
              <div className={styles.imageCard}>
                <Image
                  src="/landing.svg"
                  alt=""
                  width={960}
                  height={720}
                  priority
                  sizes="(max-width: 1024px) 100vw, 50vw"
                  className={styles.heroImg}
                />
              </div>
            </div>
          </div>

          {/* Quick links section (optional, simple and airy) */}
          <nav className={styles.quickLinks} aria-label="Accesos directos">
            <Link href="/candidates" className={styles.qLink}>
              Candidatos
              <span aria-hidden="true" className={styles.arrow}>→</span>
            </Link>
            <Link href="/noticias" className={styles.qLink}>
              Noticias
              <span aria-hidden="true" className={styles.arrow}>→</span>
            </Link>
            
          </nav>
        </div>
      </section>
    </>
  );
}
