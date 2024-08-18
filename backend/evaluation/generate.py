# from backend.schema.embedding import LangchainPGCollection, LangchainPGEmbedding
# from backend.schema.evaluation import Evaluation
# from backend.config import CONNECTION_STRING
# from sqlmodel import create_engine, Session, select
# from backend.database import SessionLocal

# import pandas as pd


# def load_embeddings_to_dataframe():
#     engine = create_engine(CONNECTION_STRING)
#     with Session(engine) as session:
#         embeddings = session.exec(select(LangchainPGEmbedding)).all()
#         embeddings_list = []
#         for embedding in embeddings:
#             embeddings_list.append(
#                 {
#                     "id": embedding.id,
#                     "collection_id": embedding.collection_id,
#                     "embedding": embedding.embedding,
#                     "document": embedding.document,
#                     "cmetadata": embedding.cmetadata,
#                 }
#             )
#         df = pd.DataFrame(embeddings_list)
#         # Extracting the keys from 'cmetadata' into separate columns
#         df_expanded = pd.concat(
#             [df.drop(columns=["cmetadata"]), df["cmetadata"].apply(pd.Series)], axis=1
#         )

#         return df_expanded


# if __name__ == "__main__":
#     df = load_embeddings_to_dataframe()
#     print(df)
