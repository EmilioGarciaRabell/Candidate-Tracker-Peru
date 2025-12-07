"use client";

import Image from "next/image";
import styles from "./metodologias.module.css";

export default function MetodologiasPage() {
  return (
    <div className={styles.pageWrapper}>
      {/* Hero / Intro */}
      <section className={`section ${styles.heroSection}`}>
        <div className="container">
          <div className={styles.breadcrumbWrapper}>
            <span className={styles.breadcrumb}>
              <a href="/" className={styles.breadcrumbLink}>
                Inicio
              </a>
              <span className={styles.breadcrumbSeparator}>/</span>
              <span className={styles.breadcrumbCurrent}>Metodologías</span>
            </span>
          </div>

          <div className={styles.heroContent}>
            <p className={styles.heroEyebrow}>Metodologías</p>
            <h1 className={`title is-1 ${styles.heroTitle}`}>
              Recolección y procesamiento<br />de información
            </h1>
            <p className={`subtitle is-5 ${styles.heroSubtitle}`}>
              Esta página explica, de manera técnica y transparente,{" "}
              cómo se recolecta, procesa y verifica la información presentada en
              la plataforma. Nuestro objetivo es ofrecer{" "}
              <strong>transparencia total</strong> sobre los métodos utilizados
              durante el desarrollo y la obtención de datos.
            </p>
          </div>
        </div>
      </section>

      {/* Overview strip */}
      <section className={`section ${styles.overviewSection}`}>
        <div className="container">
          <div className={styles.overviewGrid}>
            <div className={styles.overviewCard}>
              <p className={styles.overviewLabel}>Alcance</p>
              <h3 className={styles.overviewTitle}>¿Qué cubren estas metodologías?</h3>
              <p className={styles.bodyParagraph}>
                Explicamos cómo se obtienen los datos de partidos y candidatos,
                cómo se procesan con modelos de IA y cuáles son las limitaciones
                y controles de calidad que aplicamos.
              </p>
            </div>
            <div className={styles.overviewCard}>
              <p className={styles.overviewLabel}>Principios</p>
              <ul className={styles.overviewList}>
                <li>Automatización para reducir sesgos humanos.</li>
                <li>Uso responsable de modelos de IA.</li>
                <li>Fuentes públicas y verificables.</li>
                <li>Claridad sobre limitaciones y alcances.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Section 1 – Información general */}
      <section className={`section ${styles.mainSection}`}>
        <div className="container">
          <div className="columns is-variable is-7 is-vcentered">
            <div className="column is-6">
              <div className={styles.pillLabel}>1. Información general</div>
              <h2 className={`title is-3 ${styles.sectionTitle}`}>
                ¿Cómo recolectamos la información general?
              </h2>
              <p className={styles.bodyParagraph}>
                La información relacionada con partidos políticos y candidatos
                se recopila a partir de noticieros, fuentes públicas y listas
                oficiales difundidas durante el último semestre de 2025.
              </p>
              <p className={`${styles.bodyParagraph} ${styles.boldText}`}>
                Para garantizar consistencia y minimizar intervención humana,
                utilizamos programas automatizados que:
              </p>
              <ol className={styles.orderedList}>
                <li>Realizan búsquedas periódicas en fuentes públicas.</li>
                <li>Extraen la información relevante de manera automática.</li>
                <li>Procesan los datos iniciales.</li>
                <li>Insertan esa información directamente en nuestra base de datos.</li>
              </ol>
              <p className={styles.bodyParagraph}>
                Este proceso asegura que la información general se mantenga
                actualizada, organizada y libre de sesgos manuales.
              </p>
            </div>

            <div className="column is-5 is-offset-1">
              <div className={styles.flowCard}>
                <p className={styles.flowLabel}>Flujo resumido</p>
                <ul className={styles.flowSteps}>
                  <li>
                    <span className={styles.stepBadge}>1</span>
                    <div>
                      <p className={styles.stepTitle}>Búsqueda automatizada</p>
                      <p className={styles.stepText}>
                        Bots consultan periódicamente fuentes públicas y listas oficiales.
                      </p>
                    </div>
                  </li>
                  <li>
                    <span className={styles.stepBadge}>2</span>
                    <div>
                      <p className={styles.stepTitle}>Extracción y filtrado</p>
                      <p className={styles.stepText}>
                        Se seleccionan solo los datos relevantes para la plataforma.
                      </p>
                    </div>
                  </li>
                  <li>
                    <span className={styles.stepBadge}>3</span>
                    <div>
                      <p className={styles.stepTitle}>Normalización</p>
                      <p className={styles.stepText}>
                        Se limpian y estructuran los datos antes de almacenarlos.
                      </p>
                    </div>
                  </li>
                  <li>
                    <span className={styles.stepBadge}>4</span>
                    <div>
                      <p className={styles.stepTitle}>Carga a la base de datos</p>
                      <p className={styles.stepText}>
                        La información queda lista para ser mostrada en la aplicación.
                      </p>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2 – Información individual candidatos */}
      <section className={`section ${styles.altSection}`}>
        <div className="container">
          <div className="columns is-variable is-7 is-vcentered">
            <div className="column is-5">
              <div className={styles.pillLabel}>2. Perfiles individuales</div>
              <h2 className={`title is-3 ${styles.sectionTitle}`}>
                ¿Cómo recolectamos la información de cada candidato?
              </h2>
            </div>
            <div className="column is-6 is-offset-1">
              <p className={styles.bodyParagraph}>
                El procedimiento es similar al de la información general,
                pero más detallado y segmentado por tipo de dato:
              </p>
              <ol className={styles.orderedList}>
                <li>
                  Un programa automatizado realiza búsquedas específicas para cada
                  categoría de información (por ejemplo, biografía, polémicas,
                  trayectoria, etc.).
                </li>
                <li>
                  Se recopilan múltiples fuentes confiables que contengan datos
                  sobre el candidato (por ejemplo, Wikipedia u otros portales
                  informativos; <strong>excluyendo redes sociales</strong>).
                </li>
                <li>
                  Una vez reunidas las fuentes, se genera una distribución
                  equilibrada del contenido para evitar que una sola fuente domine
                  la información.
                </li>
                <li>
                  Todo este contenido es procesado por un{" "}
                  <strong>LLM (modelo de lenguaje de gran tamaño)</strong>, el cual:
                  <ul className={styles.subList}>
                    <li>Organiza la información.</li>
                    <li>Extrae los puntos más relevantes.</li>
                    <li>Genera los textos finales para cada categoría del perfil.</li>
                    <li>Guarda los links de donde se obtuvo la información.</li>
                  </ul>
                </li>
              </ol>
              <div className={styles.infoNote}>
                <p>
                  El LLM no crea información nueva:{" "}
                  <strong>
                    solo sintetiza y organiza los datos provenientes de las
                    fuentes recopiladas automáticamente.
                  </strong>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Diagram 1 */}
      <section className={`section ${styles.diagramSection}`}>
        <div className="container">
          <div className={styles.diagramCard}>
            <h3 className={styles.diagramTitle}>
              3. Diagrama del proceso: Recolección de información de candidatos
            </h3>
            <p className={styles.diagramSubtitle}>
              Este flujo ilustra cómo combinamos automatización, múltiples fuentes
              y modelos de lenguaje para construir los perfiles.
            </p>
            <div className={styles.diagramWrapper}>
              <Image
                src="/diagrams/CandidateInfo.svg"
                alt="Diagrama de recolección de información de candidatos"
                width={1200}
                height={600}
                className={styles.diagramImg}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Section 4 – Sentiment analysis */}
      <section className={`section ${styles.mainSection}`}>
        <div className="container">
          <div className={styles.pillLabel}>4. Análisis de sentimiento</div>
          <div className="columns is-variable is-7 is-vcentered">
            <div className="column is-7">
              <h2 className={`title is-3 ${styles.sectionTitle}`}>
                ¿Cómo realizamos el análisis de sentimiento público?
              </h2>
              <p className={styles.bodyParagraph}>
                El análisis de sentimiento es uno de los procesos más complejos.
                Para ello:
              </p>
              <ol className={styles.orderedList}>
                <li>
                  Se recopilan comentarios exclusivamente de{" "}
                  <strong>Twitter</strong> y <strong>Reddit</strong>, publicados
                  únicamente durante <strong>la última semana</strong> para cada
                  candidato.
                </li>
                <li>
                  Los comentarios se clasifican según su tono:
                  <strong> positivo</strong>, <strong>neutral</strong> o
                  <strong> negativo</strong>.
                </li>
                <li>
                  Para este análisis utilizamos un modelo de{" "}
                  <strong>transformers</strong> llamado{" "}
                  <strong>AutoModelForSequenceClassification</strong>,
                  desarrollado por terceros (no por nuestro equipo).
                </li>
                <li>Este modelo determina automáticamente el sentimiento de cada comentario.</li>
                <li>
                  Finalmente, todos los resultados se procesan con un{" "}
                  <strong>LLM</strong>, cuya única función es:
                  <ul className={styles.subList}>
                    <li>Resumir tendencias.</li>
                    <li>Describir el tono general del público hacia el candidato.</li>
                    <li>Generar un resumen final claro para presentar en la aplicación.</li>
                  </ul>
                </li>
              </ol>
            </div>

            <div className="column is-5">
              <div className={styles.sentimentCard}>
                <p className={styles.sentimentLabel}>Rol del LLM</p>
                <p className={styles.bodyParagraph}>
                  El <strong>LLM</strong> no modifica el resultado del modelo de
                  clasificación:
                </p>
                <ul className={styles.bulletList}>
                  <li>
                    No cambia etiquetas positivas, neutrales o negativas.
                  </li>
                  <li>
                    No corrige ni ajusta los scores del modelo base.
                  </li>
                  <li>
                    Solo genera una narrativa legible sobre las tendencias.
                  </li>
                </ul>
                <p className={styles.bodyParagraph}>
                  En otras palabras, actúa como un{" "}
                  <strong>intérprete de resultados</strong>, no como un
                  juez adicional.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Diagram 2 */}
      <section className={`section ${styles.diagramSectionAlt}`}>
        <div className="container">
          <div className={styles.diagramCard}>
            <h3 className={styles.diagramTitle}>
              5. Diagrama del proceso: Análisis de sentimiento
            </h3>
            <p className={styles.diagramSubtitle}>
              Del comentario en redes sociales al resumen de percepción pública
              que ves en la plataforma.
            </p>
            <div className={styles.diagramWrapper}>
              <Image
                src="/diagrams/SentimentAnalysis.svg"
                alt="Diagrama de análisis de sentimiento"
                width={1200}
                height={600}
                className={styles.diagramImg}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Limitations & QC block grid */}
      <section className={`section ${styles.mainSection}`}>
        <div className="container">
          <div className={styles.sectionIntro}>
            <div className={styles.pillLabel}>Limitaciones y control</div>
            <h2 className={`title is-3 ${styles.sectionTitle}`}>
              Lo que sí hacemos, lo que no hacemos
            </h2>
            <p className={styles.sectionIntroText}>
              Es importante entender qué tan lejos llegan nuestros modelos y
              procesos automatizados, y cuáles son sus límites.
            </p>
          </div>

          <div className="columns is-variable is-6">
            {/* Limitaciones de las fuentes */}
            <div className="column">
              <div className={styles.storyCard}>
                <h3 className={styles.cardTitle}>
                  7. Limitaciones de las fuentes de información
                </h3>
                <p className={styles.bodyParagraph}>
                  Toda la información utilizada por esta plataforma proviene de
                  fuentes públicas disponibles en internet. Sin embargo, no todos
                  los candidatos o partidos cuentan con presencia pública
                  suficiente o información ampliamente documentada.
                </p>
                <p className={styles.bodyParagraph}>
                  Por esta razón, es posible que algunos perfiles aparezcan
                  incompletos o vacíos. La ausencia de información en un perfil
                  no implica ninguna valoración, sino simplemente una
                  limitación en la disponibilidad de datos públicos.
                </p>
              </div>
            </div>

            {/* Verificación manual */}
            <div className="column">
              <div className={styles.storyCard}>
                <h3 className={styles.cardTitle}>
                  8. Verificación manual y control de calidad
                </h3>
                <p className={styles.bodyParagraph}>
                  Aunque gran parte del proceso está automatizado, aplicamos una
                  verificación manual en los siguientes casos:
                </p>
                <ul className={styles.bulletList}>
                  <li>Información que parece inconsistente o contradictoria.</li>
                  <li>Señales de posibles errores generados por modelos de IA.</li>
                  <li>Reportes enviados por los usuarios.</li>
                  <li>Solicitudes de corrección por parte de candidatos o partidos.</li>
                </ul>
                <p className={styles.bodyParagraph}>
                  Este proceso busca mantener la plataforma precisa, neutral y
                  transparente. Cualquier solicitud enviada será verificada; de lo
                  contrario, no podrá incorporarse a la plataforma.
                </p>
              </div>
            </div>
          </div>

          {/* Limitaciones del análisis automatizado */}
          <div className={styles.limitationsBand}>
            <h3 className={styles.bandTitle}>9. Limitaciones del análisis automatizado</h3>
            <p className={styles.bodyParagraph}>
              El análisis de sentimiento y los resúmenes generados por modelos de
              inteligencia artificial:
            </p>
            <ul className={styles.bulletList}>
              <li>No representan hechos objetivos.</li>
              <li>Reflejan únicamente tendencias generales en comentarios públicos.</li>
              <li>No constituyen asesoramiento político ni recomendaciones de voto.</li>
            </ul>
            <p className={styles.bodyParagraph}>
              Esta plataforma no busca influir en la opinión pública, sino
              ofrecer herramientas informativas de forma neutral.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
