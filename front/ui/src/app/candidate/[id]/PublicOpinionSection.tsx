import React, { useEffect, useState } from "react";
import styles from "./PublicOpinionSection.module.css";

interface SentimentData {
  positive: number;
  negative: number;
  neutral: number;
  title: string;
  content: string;
}

interface Props {
  candidateId: number;
}

const PublicOpinionSection: React.FC<Props> = ({ candidateId }) => {
  const [sentiment, setSentiment] = useState<SentimentData | null>(null);
  const [loading, setLoading] = useState(true);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "";

  useEffect(() => {
    const url = apiUrl
      ? `${apiUrl}/candidate/sentiment/${candidateId}`
      : `/candidate/sentiment/${candidateId}`;

    const load = async () => {
      try {
        const res = await fetch(url, { cache: "no-store" });
        const text = await res.text();
        const parsed = JSON.parse(text);
        setSentiment(parsed.sentiment ?? null);
      } catch {
        setSentiment(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [candidateId, apiUrl]);

  if (loading) return <p>Cargando datos…</p>;
  if (!sentiment) return <p>No hay datos disponibles.</p>;

  const { positive, neutral, negative } = sentiment;
  const total = positive + neutral + negative || 1;

  const posPct = (positive / total) * 100;
  const neuPct = (neutral / total) * 100;
  const negPct = (negative / total) * 100;

  const overall = (() => {
    if (posPct > 60) return "Mayormente Positivo";
    if (negPct > 60) return "Mayormente Negativo";
    return "Opinión Mixta";
  })();

  return (
    <div >
      <div className={styles.headerSmall}>OPINIÓN PÚBLICA</div>
      <div className={styles.mainTitle}>{overall}</div>

      {/* Segmented bar (no text inside) */}
      <div className={styles.barContainer}>
        <div className={styles.segmentNegative} style={{ width: `${negPct}%` }} />
        <div className={styles.segmentNeutral} style={{ width: `${neuPct}%` }} />
        <div className={styles.segmentPositive} style={{ width: `${posPct}%` }} />
      </div>

      {/* Sentiment numbers */}
      <div className={styles.statsRow}>
        <div className={styles.stat}>
          <span className={styles.label}>Negativo</span>
          <span className={styles.value}>{negative}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.label}>Neutral</span>
          <span className={styles.value}>{neutral}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.label}>Positivo</span>
          <span className={styles.value}>{positive}</span>
        </div>
      </div>

      {/* Article */}
      {(sentiment.title || sentiment.content) && (
        <div className={styles.article}>
          {sentiment.title && <h4 className={styles.articleTitle}>{sentiment.title}</h4>}
          {sentiment.content && <p className={styles.articleText}>{sentiment.content}</p>}
        </div>
      )}
    </div>
  );
};

export default PublicOpinionSection;
