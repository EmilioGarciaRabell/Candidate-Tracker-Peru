export interface CandidateRef{
    quote: string,
    link: string
}


export interface Candidate {
    age: number;
    id: number;
    name: string;
    party: string;
    party_id:number
    ref: CandidateRef[];
    summary: string;
    experienciaLaboral: string;
    polemicas: string;
    education : string;
}
