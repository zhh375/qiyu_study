import pandas as pd
import os


def read_excel(file_path):
    df = pd.read_excel(file_path)
    data = df.to_dict('records')
    return data


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data\\cn_word\\cn_word_excel.xlsx')
    print(read_excel(path))