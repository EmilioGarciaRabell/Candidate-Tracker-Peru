export interface CandidateRef {
  quote: string;
  link: string;
  category: string;
}

export type CandidateRefs = CandidateRef[];  // <-- Array, not dictionary


export interface Candidate {
    age: number;
    id: number;
    name: string;
    party: string;
    party_id:number
    ref: CandidateRefs;
    summary: string;
    work_experience: string;
    work_experience_2: string;
    polemicas: string;
    education : string;
    education_1 : string;
}
