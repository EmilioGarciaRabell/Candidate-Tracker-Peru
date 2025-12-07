"use client";

import React from "react";
import styles from "./contact.module.css";

export default function ContactPage() {
  return (
    <section className={`section ${styles.contactSection}`}>
      <div className="container">
        <div className={styles.cardWrapper}>
          <div className={`columns is-variable is-7 ${styles.columns}`}>
            {/* Left side: copy + info */}
            <div className="column is-5">
              <div className={styles.leftPane}>
                <p className={styles.eyebrow}>Contacto</p>
                <h1 className={`title is-2 ${styles.title}`}>
                  Ponte en contacto
                </h1>

                <p className={styles.subtitle}>
                  Nos gustaría saber de ti. Si tienes preguntas, comentarios
                  o sugerencias sobre la plataforma, puedes escribirnos usando
                  este formulario.
                </p>

                <div className={styles.infoBlock}>
                  <p className={styles.infoLabel}>Correo electrónico</p>
                  <a
                    href="mailto:contacto@informate.pe"
                    className={styles.infoLink}
                  >
                    contacto@informate.pe
                  </a>
                </div>

                <div className={styles.infoBlock}>
                  <p className={styles.infoLabel}>
                    Preguntas frecuentes
                  </p>
                  <p className={styles.infoText}>
                    Antes de escribirnos, puedes revisar la sección de{" "}
                    <a href="/faq" className={styles.infoLink}>
                      Preguntas frecuentes
                    </a>{" "}
                    para ver si tu duda ya está resuelta.
                  </p>
                </div>
              </div>
            </div>

            {/* Right side: form */}
            <div className="column is-7">
              <form className={styles.form}>
                <div className="columns is-variable is-2">
                  <div className="column">
                    <div className="field">
                      <label className={`label ${styles.label}`}>
                        Nombre
                      </label>
                      <div className="control">
                        <input
                          className={`input ${styles.input}`}
                          type="text"
                          name="firstName"
                          placeholder="Tu nombre"
                        />
                      </div>
                    </div>
                  </div>
                  <div className="column">
                    <div className="field">
                      <label className={`label ${styles.label}`}>
                        Apellidos
                      </label>
                      <div className="control">
                        <input
                          className={`input ${styles.input}`}
                          type="text"
                          name="lastName"
                          placeholder="Tus apellidos"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="field">
                  <label className={`label ${styles.label}`}>
                    Correo electrónico *
                  </label>
                  <div className="control">
                    <input
                      className={`input ${styles.input}`}
                      type="email"
                      name="email"
                      placeholder="tucorreo@ejemplo.com"
                      required
                    />
                  </div>
                </div>

                <div className="field">
                  <label className={`label ${styles.label}`}>
                    Asunto
                  </label>
                  <div className="control">
                    <input
                      className={`input ${styles.input}`}
                      type="text"
                      name="subject"
                      placeholder="Motivo del mensaje"
                    />
                  </div>
                </div>

                <div className="field">
                  <label className={`label ${styles.label}`}>
                    Mensaje
                  </label>
                  <div className="control">
                    <textarea
                      className={`textarea ${styles.textarea}`}
                      name="message"
                      placeholder="Escribe tu mensaje aquí..."
                      rows={5}
                    />
                  </div>
                </div>

                <div className={styles.footerRow}>
                  <p className={styles.helperText}>
                    Intentaremos responder a tu mensaje lo antes posible.
                  </p>
                  <button
                    type="submit"
                    className={`button is-primary ${styles.submitButton}`}
                  >
                    Enviar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
