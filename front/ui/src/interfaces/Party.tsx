import { Candidate } from "./CandidateInterface";

export interface Party{
    id: number
    name:String,
    political_spectrum:String,
    summary:String
}

type ObjectProps = Party | Candidate;

export default ObjectProps;
