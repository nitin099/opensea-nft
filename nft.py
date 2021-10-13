import requests
import json
import pandas as pd
import streamlit as st
from web3 import Web3


endpoint = st.sidebar.selectbox('Endpoints', ['Assets', 'Events', 'Rarity'])


st.write(f'Opensea NFT API Explorer - {endpoint}')

st.sidebar.subheader("Filters")


if endpoint == 'Assets':
    collection = st.sidebar.text_input('Collection') or 'cryptopunks'
    params = {
        'collection': collection,
        'limit': 5
    }

    response = requests.get('https://api.opensea.io/api/v1/assets', params=params).json()

    for asset in response['assets']:
        if asset['name']:
            st.write(asset['name'])
        else:
            st.write(f"{asset['collection']['name']} - #{asset['token_id']}")

        if asset['image_url'].endswith('mp4'):
            st.video(asset['image_url'])
        else:
            st.image(asset['image_url'])

    # st.write(response)


if endpoint == 'Rarity':
    with open('assets.json') as f:
        data = json.loads(f.read())
        asset_rarities = []

        for asset in data['assets']:
            continue


if endpoint == 'Events':
    params = {}
    collection = st.sidebar.text_input('Collection')
    asset_contact_address = st.sidebar.text_input('Contract Address')
    token_id = st.sidebar.text_input('Token ID')

    # The event type to filter. Can be created for new auctions, successful for sales,
    # cancelled, bid_entered, bid_withdrawn, transfer, or approve
    event_type = st.sidebar.selectbox('Event Type', ['offer_entered', 'cancelled', 'bid_withdrawn',
                                                     'transfer', 'approve'])
    if collection:
        params['collection_slug'] = collection

    if asset_contact_address:
        params['asset_contact_address'] = asset_contact_address

    if token_id:
        params['token_id'] = token_id

    if event_type:
        params['event_type'] = event_type
    response = requests.get('https://api.opensea.io/api/v1/events', params=params).json()
    print(response)

    event_list = []
    for event in response['asset_events']:
        if event_type == 'offer_entered':
            if event['bid_amount']:
                bid_amount = Web3.fromWei(int(event['bid_amount']), 'ether')

            if event['from_account']['user']:
                bidder = event['from_account']['user']['username']

            else:
                bidder = event['from_account']['address']

            event_list.append([event['created_date'], bidder, float(bid_amount),
                               event['asset']['collection']['name'], event['asset']['token_id']])

    df = pd.DataFrame(event_list, columns=['time', 'bidder', 'bid_amount', 'collection', 'token_id'])

    st.write(df)
