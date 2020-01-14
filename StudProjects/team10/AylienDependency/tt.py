from AylienDependency.ayilien import AYLIENClient

query = "I want something easy"
text_api = AYLIENClient()
responseEntities = text_api.get_tweet_entities(query)
responseHashTags = text_api.get_tweet_HashTags(query)
list_locations = responseEntities["entities"]["location"]