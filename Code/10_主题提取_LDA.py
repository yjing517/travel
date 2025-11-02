import pandas as pd
import sys
sys.path.append("../..")
from tqdm import tqdm


if __name__ == '__main__':
    aid_df = pd.read_csv(f"../List/aid_list.csv")

