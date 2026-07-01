"""
知识库
"""
import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config
import hashlib

from ithiema.RAG项目案例.config_data import persist_directory


def check_md5(md5_str: str):
    if not os.path.exists(config.md5):
        open(config.md5, "w", encoding="utf-8").close()
        return  False
    else:
        for line in open(config.md5, "r", encoding="utf-8").readlines():
            line =line.strip()
            if line == md5_str:
                return True
        return  False

def save_md5(md5_str: str ):
    with open(config.md5, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")

def get_string_md5(input_str:str,encoding="utf-8"):
    str_bytes = input_str.encode(encoding)

    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()

class KnowledgeBase(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory = config.persist_directory
        )

if __name__ == '__main__':
    r1 = get_string_md5("hello world")
    r2 = get_string_md5("hello world")

    print(r1)
    print(r2)