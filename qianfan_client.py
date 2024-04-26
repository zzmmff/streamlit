import os

import qianfan as qf


def complete(prompt="你好"):
    os.environ["QIANFAN_ACCESS_KEY"] = "ALTAKLyd5EswPU4vMBM3eC6C8U"
    os.environ["QIANFAN_SECRET_KEY"] = "f6e9da6c27aa41f09936dc98e60d414e"
    comp = qf.Completion()
    resp = comp.do(model="ERNIE-Bot", prompt=prompt)
    result = resp.body.get("result")
    return result
