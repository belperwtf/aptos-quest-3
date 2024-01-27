def map_edition_launch(response):
    if not response.get('data') or not response['data'].get('aptos'):
        return []

    launch = response['data']['aptos'].get('edition_launches', [])[0]

    mapped_data = {
            'token_id': launch.get('token_id'),
            'collection_slug': launch.get('collection_slug'),
            'creator': launch.get('creator')
        }

    return mapped_data
