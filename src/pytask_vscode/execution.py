import pytask
import json
from multiprocessing.connection import Client


@pytask.hookimpl(tryfirst=True)
def pytask_execute_task_log_end(session: pytask.Session, report: pytask.ExecutionReport) -> None:
    try:
        if not session.config["dry_run"]:
            attrs = {"type" : "task" ,"name" : report.task.short_name, "path" : str(report.task.path), "report" : str(report.outcome)}
            address = ('localhost', 6000)
            conn = Client(address, authkey=b'secret password')
            conn.send(json.dumps(attrs))
            conn.close()
    except Exception as e:
        pass
@pytask.hookimpl
def pytask_execute_log_end(session: pytask.Session, reports: list[pytask.ExecutionReport]) -> None:
    try:
        if  not session.config["dry_run"]:
            address = ('localhost', 6000)
            conn = Client(address, authkey=b'secret password')
            conn.send('close')
            conn.close()
    except Exception as e:
        pass