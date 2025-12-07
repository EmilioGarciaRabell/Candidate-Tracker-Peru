"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import styles from "./navbar.module.css";
import "bulma/css/bulma.min.css";

const navItems = [
  { href: "/candidates", label: "Candidatos" },
  { href: "/parties", label: "Partidos" },
  { href: "/noticias", label: "Noticias" },
  { href: "/dashboard", label: "Tendencias" },
  { href: "/metodologias", label: "Metodologías" },
  { href: "/faq", label: "Preguntas Frequentes" },
  { href: "/about", label: "Acerca de" },
  { href: "/contact", label: "Contactanos" },
  
  
  
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 6);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={styles.headerWrap}>
      <nav
        className={`navbar ${styles.navbarLight} ${scrolled ? styles.scrolled : ""}`}
        role="navigation"
        aria-label="main navigation"
      >
        <div className="container">
          <div className="navbar-brand">
            <Link href="/" className={`navbar-item ${styles.logoLink}`} aria-label="Inicio">
              <Image
                src="/logo.svg"
                alt="Logo"
                width={72}
                height={72}
                className={styles.logoImg}
                priority
              />
            </Link>

            <button
              className={`navbar-burger ${open ? "is-active" : ""}`}
              aria-label="Abrir menú"
              aria-expanded={open}
              onClick={() => setOpen((v) => !v)}
              type="button"
            >
              <span aria-hidden="true" />
              <span aria-hidden="true" />
              <span aria-hidden="true" />
            </button>
          </div>

          <div className={`navbar-menu ${open ? "is-active" : ""}`}>
            <div className={`navbar-start ${styles.navStart}`}>
              {navItems.map(({ href, label }) => {
                const isActive = href === "/" ? pathname === "/" : pathname?.startsWith(href);
                return (
                  <Link
                    key={href + label}
                    href={href}
                    className={`${styles.navItem} ${isActive ? styles.active : ""}`}
                    aria-current={isActive ? "page" : undefined}
                    onClick={() => setOpen(false)}
                  >
                    {label}
                  </Link>
                );
              })}
            </div>

            <div className="navbar-end">
              
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
}
