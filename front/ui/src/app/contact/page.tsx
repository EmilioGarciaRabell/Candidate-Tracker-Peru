"use client";

import React, { useState } from "react";
import styles from "./contact.module.css";
import { Contact } from "@/interfaces/Contact";
import "bulma/css/bulma.min.css";

export default function ContactPage() {

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  const[contact,setContact] = useState<Contact>({
      name:"",
      lastName:"",
      asunto:"",
      email:"",
      mensaje:""
  })

  const [isModalOpen, setIsModalOpen] = useState(false);


  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
      setContact((prev) => ({
        ...prev,
        [name]: value,
      }));
};

  const onSubmit = async (e:React.FormEvent) =>{
    e.preventDefault();
    console.log(contact)
    setIsModalOpen(true)

    try {
      const response = await fetch(`${apiUrl}/contact`,{
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(contact),
      })

      const data = await response.json();
      console.log('Success:', data);

    } catch (error) {
      console.log(error)
    }
  }



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
              <form className={styles.form} onSubmit={onSubmit}>
                <div className="columns is-variable is-2">
                  <div className="column">
                    <div className="field">
                      <label className={`label ${styles.label}`}>
                        Nombre
                      </label>
                      <div className="control">
                        <input
                          value={contact.name}
                          className={`input ${styles.input}`}
                          type="text"
                          name="name"
                          placeholder="Tu nombre"
                          onChange={handleOnChange}
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
                          value={contact.lastName}
                          className={`input ${styles.input}`}
                          type="text"
                          name="lastName"
                          placeholder="Tus apellidos"
                          onChange={handleOnChange}
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
                      value={contact.email}
                      className={`input ${styles.input}`}
                      type="email"
                      name="email"
                      placeholder="tucorreo@ejemplo.com"
                      required
                      onChange={handleOnChange}
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
                      name="asunto"
                      placeholder="Motivo del mensaje"
                      value={contact.asunto}
                      onChange={handleOnChange}
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
                      name="mensaje"
                      placeholder="Escribe tu mensaje aquí..."
                      rows={5}
                      value={contact.mensaje}
                      onChange={handleOnChange}
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
       {isModalOpen && (
  <div className="modal is-active">
    <div
      className={`modal-background ${styles.background}`}
      onClick={() => setIsModalOpen(false)}
    ></div>

    <div className={`modal-card ${styles.card}`}>
      <header className={`modal-card-head ${styles.header}`}>
        <p className={`modal-card-title ${styles.title}`}>Mensaje enviado</p>
      </header>

      <section className={`modal-card-body ${styles.body}`}>
        Hemos recibido tu mensaje. Nuestro equipo se comunicará contigo pronto.
      </section>

      <footer className={`modal-card-foot ${styles.footer}`}>
        <button
          className={`button is-primary ${styles.submitButton}`}
          onClick={() => setIsModalOpen(false)}
        >
          Cerrar
        </button>
      </footer>
    </div>

    <button
      className="modal-close is-large"
      aria-label="close"
      onClick={() => setIsModalOpen(false)}
    ></button>
  </div>
)}
    </section>
  );
}
