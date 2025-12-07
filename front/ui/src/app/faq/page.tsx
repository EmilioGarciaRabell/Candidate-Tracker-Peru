"use client";

import { useState } from "react";

export default function FAQPage() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const faqs = [
    {
      q: "¿Quién se beneficia de esta aplicación?",
      a: "El objetivo de esta aplicación es brindar información clara y accesible al público. Ningún miembro del equipo de desarrollo recibe actualmente compensación económica por su funcionamiento."
    },
    {
      q: "Hay información incorrecta, ¿cómo puedo reportarla?",
      a: "Puedes utilizar el formulario disponible en la página de Contáctanos. Indica qué información consideras incorrecta y revisaremos el reporte lo antes posible. Toda información enviada por el público será analizada previamente antes de realizar cualquier actualización."
    },
    {
      q: "Soy un candidato o partido y estoy inconforme con la información en mi perfil, ¿cómo lo puedo reportar?",
      a: "Si eres un candidato o representante de un partido político y deseas corregir información, utiliza el formulario en la página de Contáctanos y menciona tu rol. Será necesario verificar tu identidad antes de procesar la solicitud. Una vez verificada, la información será revisada y actualizada si corresponde.\n\nLas correcciones provenientes de candidatos o partidos serán tomadas como válidas, excepto en casos donde la información resulte falsa, propagandística o irrespetuosa."
    },
    {
      q: "¿Qué organización es dueña de esta aplicación?",
      a: "Esta aplicación fue desarrollada de manera independiente por un grupo de estudiantes, con el objetivo de informar a la ciudadanía y apoyar una mejor preparación para las próximas elecciones."
    },
    {
      q: "¿De dónde proviene la información?",
      a: "La información incluida en esta plataforma ha sido recopilada exclusivamente de fuentes públicas disponibles en internet hasta la fecha de publicación."
    },
    {
      q: "¿Cuál es su afiliación política?",
      a: "La aplicación ha sido desarrollada de manera completamente independiente. No se ha recibido ningún tipo de compensación económica ni apoyo de partidos políticos, instituciones gubernamentales o actores externos."
    },
    {
      q: "Quiero participar en el desarrollo de esta aplicación, ¿cómo puedo involucrarme?",
      a: "Nos encantaría contar con más personas en el equipo. Si te interesa contribuir a la plataforma, contáctanos a través del formulario en la página de Contáctanos. Actualmente, no podemos ofrecer compensación económica a nuevos desarrolladores o colaboradores."
    },
    {
      q: "Soy una agencia de periodismo o un periodista independiente, ¿cómo puedo contactarlos?",
      a: "Por favor, utiliza el formulario disponible en la página de Contáctanos para establecer comunicación con nuestro equipo."
    },
    {
      q: "Soy un educador o institución educativa, ¿cómo puedo contactarlos?",
      a: "El equipo de desarrollo está comprometido con la promoción de la educación y la transparencia. Si eres educador o formas parte de una institución educativa y te gustaría coordinar una charla o participación de nuestro equipo, puedes enviarnos un mensaje mediante el formulario de Contáctanos."
    },
    {
      q: "¿Por quién recomiendan votar?",
      a: "No recomendamos ni promovemos el voto por ningún candidato o partido político. La decisión de voto es personal y corresponde exclusivamente a cada ciudadano. Esta plataforma tiene como único objetivo fomentar la educación y la transparencia sobre el proceso electoral rumbo a las elecciones de 2026."
    }
  ];

  return (
    <section className="section py-4 px-3">
      <div className="container is-max-desktop">

        {/* Título */}
        <div className="has-text-centered mb-4">
          <h1 className="title is-2 has-text-weight-bold has-text-primary-dark mb-2">
            Preguntas Frecuentes
          </h1>
          <p className="subtitle is-6 has-text-grey">
            Todo lo que necesitas saber sobre la plataforma
          </p>
        </div>

        {/* Acordeón pegadito */}
        <div className="accordion">
          {faqs.map((faq, index) => (
            <article
              key={index}
              className={`message is-medium mb-2 faq-item ${openIndex === index ? "is-open" : ""}`}
              onClick={() => setOpenIndex(openIndex === index ? null : index)}
            >
              <div className="message-header has-background-info-light p-4">
                <p className="has-text-weight-bold has-text-black is-size-5">
                  {index + 1}. {faq.q}
                </p>
                <span className="icon">
                  <i className={`fas fa-chevron-${openIndex === index ? "up" : "down"} fa-lg`}></i>
                </span>
              </div>
              <div className="message-body p-4 has-background-white-bis">
                <div className="content has-text-black-bis">
                  {faq.a.split("\n\n").map((p, i) => (
                    <p key={i} className="mb-3">{p}</p>
                  ))}
                </div>
              </div>
            </article>
          ))}
        </div>

      </div>
    </section>
  );
}