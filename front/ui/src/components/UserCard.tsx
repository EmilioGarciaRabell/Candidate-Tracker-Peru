"use client";
import { useRouter } from "next/navigation";
import s from "./userCard.module.css";
import "../styles/globals.css";
import ObjectProps from "@/interfaces/Party";

export default function UserCard(props: ObjectProps) {
  const router = useRouter();

  return (
    <div className={s.card}>
      {/* Header: Name & Party */}
      <div className={s.cardHeader}>
        <h2 className={s.cardName}>{props.name}</h2>

        {"party" in props ? (
          <>
            {/* Candidate card */}
            <h4 className={s.cardParty}>Partido: {props.party}</h4>
          </>
        ) : (
          <>
            {/* Ideology card */}
            <h4 className={s.cardParty}>
              Ideología: {props.political_spectrum}
            </h4>
          </>
        )}
      </div>

      {/* Info section */}
      {"party" in props ? (
        <>
          <div className={s.cardInfo}>
            <div className={s.cardInfoItem}>
              <span>{props.age}</span>
              <span>Edad</span>
            </div>
          </div>

          <button
            className="customButton block w-full py-[10px] text-center"
            onClick={() => router.push(`/candidate/${props.id}`)}
          >
            Más Info
          </button>
        </>
      ) : (
        <>
          <div className={s.cardInfo}>
            <div className={s.cardInfoItem}>
              <span>{props.summary}</span>
              <span>Descripción</span>
            </div>
          </div>

          <button
            className="customButton block w-full py-[10px] text-center"
            onClick={() => router.push(`/party/${props.id}`)}
          >
            Más Info
          </button>
        </>
      )}
    </div>
  );
}
