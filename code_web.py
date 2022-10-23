import streamlit as st
import requests
import pandas as pd
st.title("Short Description Image Generator")
st.markdown("From a short description and based on the database from MagicPrompt-Stable-Diffusion from HuggingFace + the API of StableDiffusion; images can be created based on few words; and the algorithm is in charge of adding a more detailed description")
word = st.text_input('Short image description', '')

import requests

API_URL = "https://api-inference.huggingface.co/models/Gustavosta/MagicPrompt-Stable-Diffusion"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


if len(word)> 0:
    do_image = True
else:
    do_image = False

if do_image:
    output = query({
        "inputs": str(word),
    })

    key, value = list(output[0].items())[0]
    output = value
    st.write("Generated text:  ", output)

    import getpass, os

    # NB: host url is not prepended with \"https\" nor does it have a trailing slash.
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

    key = st.text_input('Add your DreamStudio API Key', '')
    st.markdown("For having your API key visit: https://beta.dreamstudio.ai/membership ")
    st.markdown("Otherwise you can add the obtained prompt manually to https://huggingface.co/spaces/stabilityai/stable-diffusion ")
    st.markdown(" 📌 Have you been using this app before? All the generated images have been paid to the DreamStudio app by me. If you have enjoy it and you want to invite me to a coffe you can do it here: https://paypal.me/evadeltor?country.x=ES&locale.x=es_ES")
    # To get your API key, visit https://beta.dreamstudio.ai/membership
    if len(key) > 0:
        have_key = True
    else:
        have_key = False
    if have_key:
        os.environ['STABILITY_KEY'] = str(key)
        import io
        import os
        import warnings

        from stability_sdk import client
        import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


        stability_api = client.StabilityInference(
            key=os.environ['STABILITY_KEY'],
            verbose=True,
        )

        # the object returned is a python generator
        answers = stability_api.generate(
            prompt=output
        )

        from PIL import Image


        # iterating over the generator produces the api response
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    st.image(img, caption='Image generated')




