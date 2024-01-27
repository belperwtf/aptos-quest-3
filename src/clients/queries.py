FETCH_EDITION_LAUNCH_BY_ID = """
query fetchEditionLaunchById($id: uuid!) {
    aptos {
        edition_launches(where: {
            id: {
                _eq: $id
            }
        }) {
            collection_slug
            creator
            description
            end_time
            id
            token_id
            limit
            media_type
            media_url
            name
            price
            royalty
            start_time
            supply_count
            supply_type
            minted 
            collection {
                id
                title
                slug
                cover_url
                semantic_slug
                discord
                twitter
                website
                supply
            }
        }
    }
}
"""