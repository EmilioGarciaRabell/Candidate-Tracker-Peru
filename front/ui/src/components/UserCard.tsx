"use client";

import { Candidate } from "@/interfaces/CandidateInterface";
import s from "./userCard.module.css";
import { useRouter } from "next/navigation";
import Image from "next/image";
// ⬇️ Update this path if your profile.jpg is elsewhere
import profilePicture from "./profile.jpg";

export default function UserCard({ name, party, age, id }: Candidate) {
  const router = useRouter();

  return (
    <article
      className={s.card}
      role="button"
      tabIndex={0}
      onClick={() => router.push(`/candidate/${id}`)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") router.push(`/candidate/${id}`);
      }}
    >
      {/* Avatar */}
      <div className={s.avatarWrap} aria-hidden="true">
        <div className={s.avatarRing}>
          <Image
            src={profilePicture}
            alt=""
            className={s.avatarImg}
            width={72}
            height={72}
            priority
          />
        </div>
      </div>

      {/* Title / Meta */}
      <header className={s.header}>
        <h2 className={s.name} title={name}>{name}</h2>
        <div className={s.metaRow}>
          <span className={s.chip}>
            {party ? `Partido ${party}` : "Sin partido"}
          </span>
          <span className={s.dot} />
          <span className={s.metaText}>{age ?? "—"} años</span>
        </div>
      </header>

      {/* Footer action */}
      <footer className={s.footer}>
        <button
          className={s.linkButton}
          onClick={(e) => {
            e.stopPropagation();
            router.push(`/candidate/${id}`);
          }}
        >
          Más info
          <svg
            className={s.arrow}
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            aria-hidden="true"
          >
            <path d="M5 12h14M13 5l7 7-7 7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </footer>
    </article>
  );
}
