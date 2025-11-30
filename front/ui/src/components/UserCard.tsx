"use client";

import { Candidate } from "@/interfaces/CandidateInterface";
import s from "./userCard.module.css";
import { useRouter } from "next/navigation";
import profilePicture from "./profile.jpg";
import { useEffect, useState } from "react";

type UserCardProps = Candidate & {
  onImageReady?: () => void;
};

export default function UserCard({
  name,
  party,
  age,
  id,
  onImageReady,
}: UserCardProps) {
  const router = useRouter();
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [imageFailed, setImageFailed] = useState(false);

  const safeImageSrc =
    imageFailed || !imageUrl ? profilePicture.src : imageUrl;

  useEffect(() => {
    let cancelled = false;

    const fetch_images = async () => {
      try {
        if (!apiUrl) {
          // if API URL is missing, just fall back and mark as done
          setImageFailed(true);
          return;
        }

        const res = await fetch(`${apiUrl}/image/${id}`, {
          cache: "no-store",
        });
        if (!res.ok) throw new Error("Failed image request");

        const data = await res.json();
        if (!cancelled) {
          setImageUrl(data.url);
        }
      } catch (e) {
        if (!cancelled) {
          setImageFailed(true);
        }
      } finally {
        if (!cancelled && onImageReady) {
          onImageReady();
        }
      }
    };

    fetch_images();

    return () => {
      cancelled = true;
    };
  }, [id, apiUrl, onImageReady]);

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
          <img
            src={safeImageSrc}
            onError={() => setImageFailed(true)}
            alt={`${name} profile image`}
            className={s.avatarImg}
            width={72}
            height={72}
          />
        </div>
      </div>

      {/* Title / Meta */}
      <header className={s.header}>
        <h2 className={s.name} title={name}>
          {name}
        </h2>
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
            <path
              d="M5 12h14M13 5l7 7-7 7"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </footer>
    </article>
  );
}
