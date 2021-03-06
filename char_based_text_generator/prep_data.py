import wikipedia
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['lastfm_x_wikipedia']


def get_wikipedia_band_summary(what):
    # Good examples are: 'The Beatles', 'Jihi Hendrix', 'Prince', 'Queen', and 'Japan'
    try:
        return wikipedia.page(what + ' (musician)', auto_suggest=False).summary
    except:
        try:
            return wikipedia.page(what + ' (band)', auto_suggest=False).summary
        except:
            try:
                return wikipedia.page(what, auto_suggest=False).summary
            except:
                try:
                    return wikipedia.page(what + ' (band)').summary
                except:
                    return None
            
def get_collection_name(artist):
    return artist.replace(' ', '_')

def dump_wikipedia_summary_to_mongodb(artist, linked_artists, annotate=True):
    collection = db[get_collection_name(artist)]  # Select collection
    collection.drop()  # Delete if exists
    
    for linked_artist in linked_artists:
        summary = get_wikipedia_band_summary(linked_artist)
        if summary is None:
            continue
        result = collection.insert_one({'artist': linked_artist, 
                                        'summary': summary})
        if annotate:
            print('Completed {}'.format(linked_artist))
        
    return collection

def get_concat_summary(collection):
    text = ''
    for info in collection.find():
        text += info['summary'] + '\n'
    return text

def get_collection(artist):
    return db[get_collection_name(artist)]

def print_collection_summary(collection):
    print('# of Wikipedia summaries collected: {:,}'.format(collection.count()))
    print('# of characters in all summaries: {:,}'.format(sum([len(info['summary']) for info in collection.find()])))
    print()
    print('Artists/bands: {}'.format([info['artist'] for info in collection.find()]))
    