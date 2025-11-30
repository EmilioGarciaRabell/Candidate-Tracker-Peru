import React, { useEffect, useMemo, useState } from "react";
import styles from "./PublicOpinionSection.module.css";

interface SentimentData {
  positive: number;
  negative: number;
  neutral: number;
  title?: string;
  content?: string;
}

interface Props {
  candidateId: number;
}

export default function PublicOpinionSection({ candidateId }: Props) {
  const [sentiment, setSentiment] = useState<SentimentData | null>(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";

  useEffect(() => {
    let cancelled = false;

    const url = apiUrl
      ? `${apiUrl}/candidate/sentiment/${candidateId}`
      : `/candidate/sentiment/${candidateId}`;

    const parseMaybeJson = (txt: string) => {
      try {
        return JSON.parse(txt);
      } catch {
        // fall back: try to extract numbers if server sometimes returns raw text
        return null;
      }
    };

    (async () => {
      setLoading(true);
      setErr(null);
      try {
        const res = await fetch(url, { cache: "no-store" });
        const text = await res.text();
        const parsed = parseMaybeJson(text);
        const s: SentimentData | null =
          parsed?.sentiment ?? parsed ?? null;

        if (!cancelled) setSentiment(s);
      } catch (e: any) {
        if (!cancelled) {
          setErr(e?.message || "No se pudo cargar la opinión pública.");
          setSentiment(null);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [candidateId, apiUrl]);

  const computed = useMemo(() => {
    const p = sentiment?.positive ?? 0;
    const n = sentiment?.negative ?? 0;
    const u = sentiment?.neutral ?? 0;
    const total = Math.max(p + n + u, 1); // avoid NaN
    const pct = {
      pos: (p / total) * 100,
      neg: (n / total) * 100,
      neu: (u / total) * 100,
    };
    const overall =
      pct.pos > 60 ? "Mayormente positivo"
      : pct.neg > 60 ? "Mayormente negativo"
      : "Opinión mixta";

    return { p, n, u, total, pct, overall };
  }, [sentiment]);

  const fmt = (v: number) => Intl.NumberFormat().format(v);
  const fpct = (v: number) => `${Math.round(v)}%`;

  /* ---------- States ---------- */
  if (loading) {
    return (
      <section aria-busy="true" aria-label="Opinión pública" className={styles.wrap}>
        <div className={styles.headerRow}>
          <span className={styles.kicker}>Opinión pública</span>
          <span className={styles.badgeSkeleton} />
        </div>
        <div className={styles.titleSkeleton} />
        <div className={styles.barSkeleton} />
        <div className={styles.statsSkeleton} />
      </section>
    );
  }

  if (err) {
    return (
      <section aria-live="polite" className={styles.wrap}>
        <div className={styles.headerRow}>
          <span className={styles.kicker}>Opinión pública</span>
        </div>
        <div className={styles.errorBox}>
          {err}
        </div>
      </section>
    );
  }

  if (!sentiment) {
    return (
      <section className={styles.wrap}>
        <div className={styles.headerRow}>
          <span className={styles.kicker}>Opinión pública</span>
        </div>
        <p className={styles.muted}>No hay datos disponibles.</p>
      </section>
    );
  }

  /* ---------- UI ---------- */
  return (
    <section aria-label="Opinión pública" className={styles.wrap}>
      <div className={styles.headerRow}>
        <span className={styles.kicker}>Opinión pública</span>
        <span className={styles.badge}>{computed.overall}</span>
      </div>

      {/* Segmented bar with accessible labels */}
      <figure
        className={styles.barContainer}
        role="img"
        aria-label={`Distribución: ${fpct(computed.pct.neg)} negativo, ${fpct(computed.pct.neu)} neutral, ${fpct(computed.pct.pos)} positivo`}
      >
        <div
          className={styles.segmentNegative}
          style={{ width: `${computed.pct.neg}%` }}
          aria-hidden="true"
          title={`Negativo ${fpct(computed.pct.neg)}`}
        />
        <div
          className={styles.segmentNeutral}
          style={{ width: `${computed.pct.neu}%` }}
          aria-hidden="true"
          title={`Neutral ${fpct(computed.pct.neu)}`}
        />
        <div
          className={styles.segmentPositive}
          style={{ width: `${computed.pct.pos}%` }}
          aria-hidden="true"
          title={`Positivo ${fpct(computed.pct.pos)}`}
        />
      </figure>

      {/* Legend / numbers */}
      <div className={styles.statsRow}>
        <div className={styles.stat}>
          <span className={`${styles.dot} ${styles.dotNeg}`} aria-hidden="true" />
          <span className={styles.label}>Negativo</span>
          <span className={styles.value}>
            {fmt(computed.n)} <span className={styles.pct}>({fpct(computed.pct.neg)})</span>
          </span>
        </div>
        <div className={styles.stat}>
          <span className={`${styles.dot} ${styles.dotNeu}`} aria-hidden="true" />
          <span className={styles.label}>Neutral</span>
          <span className={styles.value}>
            {fmt(computed.u)} <span className={styles.pct}>({fpct(computed.pct.neu)})</span>
          </span>
        </div>
        <div className={styles.stat}>
          <span className={`${styles.dot} ${styles.dotPos}`} aria-hidden="true" />
          <span className={styles.label}>Positivo</span>
          <span className={styles.value}>
            {fmt(computed.p)} <span className={styles.pct}>({fpct(computed.pct.pos)})</span>
          </span>
        </div>
      </div>

      {/* Optional article */}
      {(sentiment.title || sentiment.content) && (
        <article className={styles.article} aria-labelledby="op-art-title">
          {sentiment.title && <h4 id="op-art-title" className={styles.articleTitle}>{sentiment.title}</h4>}
          {sentiment.content && <p className={styles.articleText}>{sentiment.content}</p>}
        </article>
      )}
    </section>
  );
}
