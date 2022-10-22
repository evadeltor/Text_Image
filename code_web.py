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

    # To get your API key, visit https://beta.dreamstudio.ai/membership
    os.environ['STABILITY_KEY'] = "sk-YntvOaDTrTZt4t5LTz0bszZeGcgJVZia2vlbohGM7p6ji0GH"
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




