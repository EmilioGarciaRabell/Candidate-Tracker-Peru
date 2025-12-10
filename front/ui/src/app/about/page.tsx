import React from "react";
import styles from "./about.module.css";

const About: React.FC = () => {
  return (
    <div className={styles.pageWrapper}>
      {/* Hero / Intro */}
      <section className={`section ${styles.heroSection}`}>
        <div className="container">
          <div className={styles.breadcrumbWrapper}>
            <span className={styles.breadcrumb}>
              <a href="/" className={styles.breadcrumbLink}>
                Inicio
              </a>{" "}
              <span className={styles.breadcrumbSeparator}>/</span>{" "}
              <span className={styles.breadcrumbCurrent}>Acerca de</span>
            </span>
          </div>

          <div className={styles.heroContent}>
            <p className={styles.heroEyebrow}>Nuestra historia</p>
            <h1 className={`title is-1 ${styles.heroTitle}`}>
              Transparencia para las elecciones Perú 2026
            </h1>
            <p className={`subtitle is-4 ${styles.heroSubtitle}`}>
              informate.pe es una plataforma independiente creada para ayudar a
              la ciudadanía a conocer mejor a cada candidato: su trayectoria,
              sus polémicas y la percepción pública que los rodea.
            </p>
          </div>
        </div>
      </section>

      {/* Story body */}
      <section className={`section ${styles.storySection}`}>
        <div className="container">
          <div className="columns is-variable is-7 is-vcentered">
            <div className="column is-6">
              <h2 className={`title is-3 ${styles.sectionTitle}`}>
                ¿Qué es informate.pe?
              </h2>
              <p className={styles.leadParagraph}>
                Bienvenido a <strong>informate.pe</strong>. En esta plataforma
                podrás encontrar una lista detallada de todos los candidatos
                para las elecciones de Perú 2026, así como información clara,
                organizada y transparente sobre cada uno de ellos.
              </p>
              <p className={styles.bodyParagraph}>
                A cada candidato se le ha asignado un perfil individual, donde
                podrás encontrar información como su biografía, polémicas,
                análisis de sentimiento público, educación, experiencia laboral
                y fuentes de información. Para conocer más sobre cómo se realizó
                la recopilación de la información, puedes visitar la página de{" "}
                <a href="/metodologias" className={styles.textLink}>
                  Metodologías
                </a>
                .
              </p>
            </div>

            <div className="column is-5 is-offset-1">
              <div className={styles.highlightCard}>
                <p className={styles.highlightLabel}>Lo que encontrarás</p>
                <ul className={styles.highlightList}>
                  <li>Perfiles detallados de todos los candidatos.</li>
                  <li>Biografía, educación y experiencia laboral.</li>
                  <li>Polémicas y análisis de sentimiento público.</li>
                  <li>Fuentes de información claramente referenciadas.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Objective section */}
      <section className={`section ${styles.altSection}`}>
        <div className="container">
          <div className="columns is-variable is-7 is-vcentered">
            <div className="column is-5">
              <div className={styles.pillLabel}>Objetivo</div>
              <h2 className={`title is-3 ${styles.sectionTitle}`}>
                Una plataforma creada para la ciudadanía
              </h2>
            </div>
            <div className="column is-6 is-offset-1">
              <p className={styles.bodyParagraph}>
                Nuestra plataforma tiene como objetivo principal informar a la
                ciudadanía de manera totalmente transparente. Sabemos que no es
                sencillo tomar una decisión cuando existen muchas opciones y
                todos intentan captar tu atención.
              </p>
              <p className={styles.bodyParagraph}>
                Nos comprometemos a mantener el sitio libre de información
                pagada, publicidad o cualquier tipo de contenido patrocinado por
                partidos o candidatos.
              </p>
              <p className={styles.bodyParagraph}>
                Si tienes preguntas, puedes utilizar el formulario de{" "}
                <a href="/contacto" className={styles.textLink}>
                  contacto
                </a>{" "}
                para enviarnos un mensaje.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Split story section (Desarrollo + Open source) */}
      <section className={`section ${styles.storyGridSection}`}>
        <div className="container">
          <div className={styles.sectionIntro}>
            <div className={styles.pillLabel}>Detrás de la plataforma</div>
            <h2 className={`title is-3 ${styles.sectionTitle}`}>
              Desarrollo independiente y código abierto
            </h2>
            <p className={styles.sectionIntroText}>
              informate.pe fue creada por dos estudiantes sin afiliación
              política, con el objetivo de aportar más transparencia al proceso
              electoral.
            </p>
          </div>

          <div className="columns is-variable is-7">
            {/* Desarrollo */}
            <div className="column">
              <div className={styles.storyCard}>
                <h3 className={`title is-4 ${styles.cardTitle}`}>Desarrollo</h3>
                <p className={styles.bodyParagraph}>
                  El desarrollo de esta aplicación fue realizado por dos
                  estudiantes que no tienen ningún tipo de afiliación política
                  ni han recibido compensación económica o beneficios de ningún
                  tipo para crear esta plataforma.
                </p>
                <p className={styles.bodyParagraph}>
                  Asimismo, el mantenimiento y funcionamiento del sitio son
                  realizados por estos dos estudiantes, quienes asumen los
                  costos necesarios para mantener la aplicación en línea.
                </p>
                <p className={styles.bodyParagraph}>
                  La plataforma fue desarrollada utilizando{" "}
                  <strong>React</strong> para la interfaz gráfica y{" "}
                  <strong>Flask</strong> para la lógica del servidor. Además, se
                  utilizaron distintas herramientas y servicios, como{" "}
                  <strong>Google Cloud</strong> y otros servicios de terceros.
                </p>
              </div>
            </div>

            {/* Código abierto */}
            <div className="column">
              <div className={styles.storyCard}>
                <h3 className={`title is-4 ${styles.cardTitle}`}>
                  Código abierto
                </h3>
                <p className={styles.bodyParagraph}>
                  Todo el código de la plataforma es de acceso público, de modo
                  que cualquier persona puede revisar cómo está construida.
                </p>
                <p className={styles.bodyParagraph}>
                  También contamos con una página de{" "}
                  <a href="/metodologias" className={styles.textLink}>
                    Metodologías
                  </a>{" "}
                  donde se explica cómo obtenemos y procesamos la información
                  utilizada en la plataforma.
                </p>

                <div className={styles.metaCallout}>
                  <p className={styles.metaLabel}>Transparencia técnica</p>
                  <p className={styles.metaText}>
                    Al abrir el código y documentar nuestras metodologías,
                    buscamos que cualquier persona pueda auditar, cuestionar y
                    mejorar el proyecto.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Closing band */}
      <section className={`section ${styles.closingSection}`}>
        <div className="container">
          <div className={styles.closingCard}>
            <p className={styles.closingEyebrow}>Nuestro compromiso</p>
            <h2 className={`title is-4 ${styles.closingTitle}`}>
              Una decisión informada es una decisión más libre.
            </h2>
            <p className={styles.closingText}>
              informate.pe seguirá evolucionando, pero nuestro principio seguirá
              siendo el mismo: ofrecer información electoral clara, verificable
              y sin intereses ocultos, para que puedas decidir con confianza.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
