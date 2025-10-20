"use client";
import { Candidate } from "@/interfaces/CandidateInterface";
import s from "./userCard.module.css";
import { useRouter } from "next/navigation";

export default function UserCard({ name, party_id, age, id }: Candidate) {
  const router = useRouter();

  return (
    <div className={s.card}>
      {/* Header: Name & Party */}
      <div className={s.cardHeader}>
        <h2 className={s.cardName}>{name}</h2>
        <h4 className={s.cardParty}>Partido: {party_id}</h4>
      </div>

      {/* Info: Age */}
      <div className={s.cardInfo}>
        <div className={s.cardInfoItem}>
          <span>{age}</span>
          <span>Edad</span>
        </div>
      </div>

      {/* Button */}
      <button
        className={s.cardButton}
        onClick={() => router.push(`/candidate/${id}`)}
      >
        Más Info
      </button>
    </div>
  );
}
