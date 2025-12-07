"use client";

import Image from "next/image";

export default function MetodologiasPage() {
  return (
    <section className="section py-6">
      <div className="container">

        {/* Título principal */}
        <div className="block has-text-centered mb-6">
          <h1 className="title is-1 has-text-weight-bold has-text-black">
            Metodologías de Recolección y<br />Procesamiento de Información
          </h1>
        </div>

        <div className="block mb-6">
          <p className="subtitle is-5 has-text-black is-italic has-text-centered">
            Esta página tiene el propósito de explicar, de manera técnica y transparente, cómo se recolecta, procesa y verifica la información presentada en la aplicación. Nuestro objetivo es ofrecer transparencia total sobre los métodos utilizados durante el desarrollo y la obtención de datos.
          </p>
        </div>

        {/* Sección 1 */}
        <div className="box">
          <h2 className="title is-3 has-text-black">1. ¿Cómo recolectamos la información general?</h2>
          <p className="mb-4">La información relacionada con partidos políticos y candidatos se recopila a partir de noticieros, fuentes públicas y listas oficiales difundidas durante el último semestre de 2025.</p>
          <p className="has-text-weight-bold mb-4">Para garantizar consistencia y minimizar intervención humana, utilizamos programas automatizados que:</p>
          <ol className="ml-5 mb-4">
            <li className="mb-3">Realizan búsquedas periódicas en fuentes públicas.</li>
            <li className="mb-3">Extraen la información relevante de manera automática.</li>
            <li className="mb-3">Procesan los datos iniciales.</li>
            <li className="mb-3">Insertan esa información directamente en nuestra base de datos.</li>
          </ol>
          <p>Este proceso asegura que la información general se mantenga actualizada, organizada y libre de sesgos manuales.</p>
        </div>

        {/* Sección 2 */}
        <div className="box">
          <h2 className="title is-3 has-text-black">2. ¿Cómo recolectamos la información individual de cada candidato?</h2>
          <p className="mb-4">El procedimiento es similar al de la información general, pero más detallado:</p>
          <ol className="ml-5 mb-4">
            <li className="mb-3">Un programa automatizado realiza búsquedas específicas para cada categoría de información (por ejemplo, biografía, polémicas, trayectoria, etc.).</li>
            <li className="mb-3">Se recopilan múltiples fuentes confiables que contengan datos sobre el candidato (por ejemplo, Wikipedia u otros portales informativos; <strong>excluyendo redes sociales</strong>).</li>
            <li className="mb-3">Una vez reunidas las fuentes, se genera una distribución equilibrada del contenido para evitar que una sola fuente domine la información.</li>
            <li className="mb-3">
              Todo este contenido es procesado por un <strong>LLM (modelo de lenguaje de gran tamaño)</strong>, el cual:
              <ul className="ml-6 mt-3">
                <li>Organiza la información.</li>
                <li>Extrae los puntos más relevantes.</li>
                <li>Genera los textos finales para cada categoría del perfil del candidato.</li>
                <li>Y guarda los links de donde se recaudó la información.</li>
              </ul>
            </li>
          </ol>
          <div className="notification is-info is-light mt-5">
            <p className="has-text-weight-bold">El LLM no crea información nueva: <strong>solo sintetiza y organiza los datos provenientes de las fuentes recopiladas automáticamente</strong>.</p>
          </div>
        </div>

        {/* Diagrama 1 */}
        <div className="box has-background-light">
          <h3 className="title is-4 has-text-centered has-text-black">3. Diagrama del Proceso: Recolección de Información de Candidatos</h3>
          <figure className="image is-fullwidth mt-5">
            <Image
              src="/diagrams/CandidateInfo.jpg"
              alt="Diagrama de recolección"
              width={1200}
              height={600}
              className="has-ratio"
              style={{ borderRadius: "12px", boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
            />
          </figure>
        </div>

        {/* Sección 4 */}
        <div className="box">
          <h2 className="title is-3 has-text-black">4. ¿Cómo realizamos el análisis de sentimiento público?</h2>
          <p className="mb-4">El análisis de sentimiento es uno de los procesos más complejos. Para ello:</p>
          <ol className="ml-5 mb-4">
            <li className="mb-3">Se recopilan comentarios exclusivamente de <strong>Twitter</strong> y <strong>Reddit</strong>, publicados únicamente durante <strong>la última semana</strong> para cada candidato.</li>
            <li className="mb-3">Los comentarios se clasifican según su tono: <strong>positivo</strong>, <strong>neutral</strong> o <strong>negativo</strong>.</li>
            <li className="mb-3">Para este análisis utilizamos un modelo de <strong>transformers</strong> llamado <strong>AutoModelForSequenceClassification</strong>, desarrollado por terceros (no por nuestro equipo).</li>
            <li className="mb-3">Este modelo determina automáticamente el sentimiento de cada comentario.</li>
            <li className="mb-3">
              Finalmente, todos los resultados se procesan con un <strong>LLM</strong>, cuya única función es:
              <ul className="ml-6 mt-3">
                <li>Resumir tendencias.</li>
                <li>Describir el tono general del público hacia el candidato.</li>
                <li>Generar un resumen final claro para presentar en la aplicación.</li>
              </ul>
            </li>
          </ol>
          <div className="notification is-info is-light mt-5">
            <p className="has-text-weight-bold">El <strong>LLM</strong> no modifica el análisis del modelo de clasificación; solo produce un resumen legible del contenido.</p>
          </div>
        </div>

        {/* Diagrama 2 */}
        <div className="box has-background-light">
          <h3 className="title is-4 has-text-centered has-text-black">5. Diagrama del Proceso: Análisis de Sentimiento</h3>
          <figure className="image is-fullwidth mt-5">
            <Image
              src="/diagrams/SentimentAnalysis.jpg"
              alt="Diagrama de sentimiento"
              width={1200}
              height={600}
              className="has-ratio"
              style={{ borderRadius: "12px", boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
            />
          </figure>
        </div>

        {/* Limitaciones */}
        <div className="box">
          <h2 className="title is-3 has-text-black">7. Limitaciones de las fuentes de información</h2>
          <p className="mb-4">Toda la información utilizada por esta plataforma proviene de fuentes públicas disponibles en internet. Sin embargo, no todos los candidatos o partidos cuentan con presencia pública suficiente o información ampliamente documentada.</p>
          <p>Por esta razón, es posible que algunos perfiles aparezcan incompletos o vacíos. La ausencia de información en un perfil no implica ninguna valoración, sino simplemente una limitación en la disponibilidad de datos públicos.</p>
        </div>

        <div className="box">
          <h2 className="title is-3 has-text-black">8. Verificación manual y control de calidad</h2>
          <p className="mb-4">Aunque gran parte del proceso está automatizado, aplicamos una verificación manual en los siguientes casos:</p>
          <ul className="ml-5">
            <li className="mb-3">Información que parece inconsistente o contradictoria.</li>
            <li className="mb-3">Señales de posibles errores generados por modelos de IA.</li>
            <li className="mb-3">Reportes enviados por los usuarios.</li>
            <li className="mb-3">Solicitudes de corrección por parte de candidatos o partidos.</li>
          </ul>
          <p className="mt-4">Este proceso tiene como objetivo mantener la plataforma precisa, neutral y transparente. Es importante notar que cualquier solicitud enviada será verificada y de no ser así no se podrá incluir la petición original en la plataforma.</p>
        </div>

        <div className="box">
          <h2 className="title is-3 has-text-black">9. Limitaciones del análisis automatizado</h2>
          <p className="mb-4">El análisis de sentimiento y los resúmenes generados por modelos de inteligencia artificial:</p>
          <ul className="ml-5">
            <li className="mb-3">No representan hechos objetivos.</li>
            <li className="mb-3">Reflejan únicamente tendencias generales encontradas en comentarios públicos.</li>
            <li className="mb-3">No constituyen asesoramiento político ni recomendaciones de voto.</li>
          </ul>
          <p className="mt-4">Esta plataforma no busca influir en la opinión pública, sino ofrecer herramientas informativas de forma neutral.</p>
        </div>

      </div>
    </section>
  );
}