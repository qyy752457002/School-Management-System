
from fastapi import FastAPI, Path, HTTPException, status, Body, Form, File, UploadFile, Query

app = FastAPI()


@app.post("/prepare")
async def prepare(  ):
    return {'status':  'prepared','pre_commit_url':'precommit','rollback_url':'prerollback','commit_url':'ultracommit'}

    # return {'status':  'prepared','pre_commit_url':'precommit','rollback_url':'prerollback'}
@app.post("/precommit")
async def precommit(  ):
    return {'status':  'prepared','commit_url':'ultracommit'}
@app.post("/ultracommit")
async def ultracommit(  ):
    return {'status':  'committed','pre_commit_url':''}

@app.post("/prerollback")
async def prerollback(  ):
    return {'status':  'rollbacked','pre_commit_url':''}


# 启动应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5003)
