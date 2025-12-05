export interface NewsItem{
    link:string,
    title: string,
    keywords: string [] 
}

export interface News{
    id: number,
    name: string | undefined,
    news: NewsItem[]
}