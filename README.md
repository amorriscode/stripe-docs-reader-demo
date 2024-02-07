# StripeDocsLoader Demo

This repo contains an example of using the LlamaIndex [StripeDocsReader](https://llamahub.ai/l/stripe_docs). This loader iterates through Stripe's sitemap and consumes all of the documentation allowing users to create embeddings from them and then do RAG on those embeddings.

_Note: This demo is likely not better than GPT. The RAG approach does not utilize any of the customization that LlamaIndex provides. GPT is also already trained on this content._

## Set up

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Set up your `.env` file

```bash
cp ./.env.example ./.env
```

3. Add your Open AI API key to your `.env`

4. Create a free [Pinecode](https://www.pinecone.io/) account and add the API key to your `.env`

## Building the index from Stripe docs

```bash
python build.py
```

The `build.py` script will iterate through all of the Stripe docs using the `StripeDocsLoader`. Once it iterates through them, it will create embeddings with Open AI's ada model and upload them to Pinecone.

This process can take 3-4 hours so you'll have to be patient!

One thing to note, sometimes the Stripe sitemap 404s. If that happens, just run the script again. I'll fix this upstream in the future.

## Querying the index

```bash
python query.py
```

Once `build.py` has completed, you can run `query.py` to interact with it. You'll also be able to explore your index in the Pinecone interface.
