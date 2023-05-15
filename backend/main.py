import fastapi
import logging
import re
import uvicorn
import sqlite3
import typing
from fastapi.middleware.cors import CORSMiddleware

db = sqlite3.connect("db.sqlite", check_same_thread=False,
                     isolation_level=None)  # autocommit

db.execute("PRAGMA journal_mode=WAL")  # concurrency

db.execute(
    '''
    CREATE TABLE IF NOT EXISTS user (
        id              INTEGER     PRIMARY KEY AUTOINCREMENT,
        name            TEXT        NOT NULL,
        student_id      TEXT        NOT NULL,
        account         TEXT        NOT NULL,
        phone_number    TEXT        NOT NULL,
        discord_id      TEXT        NOT NULL,
        joined_at       TIMESTAMP   NOT NULL DEFAULT (datetime('now', 'localtime')),
        UNIQUE (student_id, discord_id)
    )
    '''
)

db.execute(
    '''
    CREATE TABLE IF NOT EXISTS record (
        timestamp       TEXT        NOT NULL,
        deptor_id       INTEGER     NOT NULL,
        creditor_id     INTEGER     NOT NULL,
        money_id        INTEGER     NOT NULL,
        memo            TEXT        DEFAULT NULL,
        UNIQUE (timestamp, deptor_id, creditor_id),
        FOREIGN KEY (deptor_id) REFERENCES user(id),
        FOREIGN KEY (creditor_id) REFERENCES user(id)
    )
    '''
)


def insert_user(name: str, account: str, phone_number: str, discord_id: str):
    db.execute(
        '''
        INSERT INTO user (name, account, phone_number, discord_id)
        VALUE (?, ?, ?, ?)
        ''', (name, account, phone_number, discord_id)
    )

def insert_record(deptor: str, creditor: str, phone_number: str, discord_id: str):
    tx = db.Cursor()
    tx: sqlite3.Cursor
    tx.execute(
        '''
        SELECT id
        FROM user
        WHERE 
        '''
    )
    tx.execute()
    tx.execute()
    tx.execute()
    tx.execute(
        '''
        INSERT INTO record (deptor_id, creditor_id, money_id, memo)
        VALUE (?, ?, ?, ?)
        ''', (deptor, account, phone_number, discord_id)
    )

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    path="/api/resource",
    description="백엔드 리소스를 읽어옵니다",
    response_class=fastapi.responses.JSONResponse,
)
def getResource(request: typing.List[str] = fastapi.Query(None)) \
        -> typing.Dict[str, typing.Union[int, str, typing.List[typing.Union[int, str]]]]:
    pass


@app.post(
    path="/api/task/control",
    description="frontend에서 쓰는 API입니다. 주어진 요청 타입에 따라 다르게 동작합니다",
    response_class=fastapi.responses.JSONResponse,
)
def taskFunctionUserSide(request: str = fastapi.Query(''), payload: dict = fastapi.Body({})):
    # 삽입
    if request == "insert":
        result = db.execute(
            """
            INSERT INTO tasks (argument, stdin)
            VALUES (?, ?)
            RETURNING id
            """,
            (payload['argument'], payload['stdin']))
        result: sqlite3.Cursor
        taskID = result.fetchall()[0][0]
        return {"taskID": taskID}

    # 삭제
    if request == "delete":
        taskID = payload['taskID']
        tx = db.cursor()
        try:
            result = tx.execute(
                "SELECT status FROM tasks WHERE id == ?", (taskID,))
            status = result.fetchall()[0][0]
            if status == "started":
                # started -> cancel_wait
                tx.execute(
                    'UPDATE tasks SET status = "cancel_wait" WHERE id = ?', (taskID,))
            elif status == "pending" or status == "success" or status == "failure":
                # pending -> NULL
                tx.execute("DELETE FROM tasks WHERE id = ?", (taskID,))
            else:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="wrong delete (invalid status of task")
        except db.Error:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="wrong delete")

        return


@app.post(
    path="/api/task/process",
    description="worker 들이 쓰는 API입니다. 주어진 요청 타입에 따라 다르게 동작합니다",
    response_class=fastapi.responses.JSONResponse,
)
def taskFunctionWorkerSide(request: str = fastapi.Query(''), payload: dict = fastapi.Body({})):
    # 처리되지 않은 태스크를 받아온다
    if request == "get":
        tx = db.cursor()
        try:
            result = tx.execute("""
                        SELECT		id, argument, stdin
                        FROM		tasks
                        WHERE		status = "pending"
                        ORDER BY	whenQueued      ASC
                        LIMIT 		1
                        """).fetchall()

            if len(result) == 0:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="nothing to process (no pending task in system)")

            taskID, argument, stdin = result[0]

            # pending -> started
            tx.execute(
                """
                    UPDATE tasks
                    SET
                        status              = "started",
                        whenStarted         = datetime('now', 'localtime'),
                        workerHostname      = ?,
                        workerProcessID     = ?
                    WHERE tasks.id = ?
                """,
                # RETURNING tasks.id, tasks.argument, tasks.stdin
                (payload["workerHostname"], payload["workerProcessID"],
                 taskID)
            )
            return {"taskID": taskID, "argument": argument, "stdin": stdin}

        except db.Error:
            raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND,
                                        detail="nothing to process (no pending task in system)")

    # 태스크 상태를 보고한다
    if request == "set":
        status = payload['status']
        taskID = payload['taskID']
        workerHostname = payload['workerHostname']
        workerProcessID = payload['workerProcessID']

        if status == 'giveup':
            # started, cancel_wait -> pending
            db.execute(
                """
                UPDATE tasks
                SET
                    status				= "pending",
                    whenStarted		    = NULL,
                    whenEnded			= NULL,
                    workerHostname		= NULL,
                    workerProcessID	    = NULL,
                    stdout				= NULL,
                    stderr				= NULL
                WHERE
                    id				    = ?         AND
                    (status	= "started" OR status = "cancel_wait") AND
                    workerHostname		= ?         AND
                    workerProcessID	    = ?
            """,
                (taskID, workerHostname, workerProcessID))

        if status == 'success' or status == 'failure':
            stdout = payload['stdout']
            stderr = payload['stderr']
            # started -> success, failure
            db.execute(
                """
                UPDATE tasks
                SET
                    status		= ?,
                    whenEnded	= datetime('now', 'localtime'),
                    stdout		= ?,
                    stderr		= ?
                WHERE
                    id  				= ?         AND
                    status				= "started" AND
                    workerHostname		= ?         AND
                    workerProcessID	    = ?
            """,
                (status, stdout, stderr,
                 taskID, workerHostname, workerProcessID))

    # cancel_wait 상태인지 체크하는 API
    if request == "check":
        result = db.execute(
            "SELECT status FROM tasks WHERE id == ?", (taskID,))
        status = result.fetchall()[0][0]
        return status


# /api/task/process?request=get 에 대해 log를 억제하기 위한 용도
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("POST /api/task/process?request=get") == -1


if __name__ == '__main__':
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
    # uvicorn.run("broker:app", host="0.0.0.0", port=8888, reload=True)
    uvicorn.run("main:app", host="127.0.0.1", port=8888, reload=True)
