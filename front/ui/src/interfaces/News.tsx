export interface NewsItem{
    fetch_date: Date
    link:string,
    title: string,
}

export interface News{
    candidate_id: number,
    news_json: NewsItem[];
    name: string | undefined
    
}