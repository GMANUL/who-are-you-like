import os
import pandas as pd

class NameById:
    def __init__(self, df_path: str):
        self.metadata_df = self.load_dataframe(df_path)

    def load_dataframe(self, path) -> pd.DataFrame:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Embedding file {path} not found")
        dataframe = pd.read_csv(path)
        return dataframe
    
    def get_celebrity_name(self, celeb_id: int) -> str:
        celeb_data = self.metadata_df[self.metadata_df['id'] == celeb_id]
        celeb_name = celeb_data['name'].squeeze()
        return celeb_name