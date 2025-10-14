def main():
    sources = get_news_srcs()
    names = get_items_names(table)

    for source in sources:
        for name in names:   
            latest_news = get_news_from_src(source, name)
            store_latest_news(name, latest_news) # local: DB, json, etc..

def get_news_srcs():
    return # all the peru news sources

def get_items_names(table):
    return # return the contents of the desired table

def get_news_from_src(source,name):
    return # get the news from the source that have the desired name in the keywords/headers

def store_latest_news(name, latests_news):
    # dataset is stored locally

    # access dataset
    dataset = dataset_connection() # connects to the dataset - write and read operations
    dataset_update_row(name, latests_news)
        # if latest_news:
            # update name latest_news
        # for any news that are not from the current week/month remove them

    return # ok or not