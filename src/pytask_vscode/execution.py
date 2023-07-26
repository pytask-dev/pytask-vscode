import pytask
import json
import requests

@pytask.hookimpl(tryfirst=True)
def pytask_collect_log(session: pytask.Session, reports: list[pytask.CollectionReport], tasks: list[pytask.Task]) -> None:
        try:    
            if session.config['command'] == 'collect':
                result = [{'name' : task.short_name, 'path' : str(task.path)} for task in tasks]
                res = requests.post('http://localhost:6000/pytask', json={"exitcode" : session.exit_code, "tasks": result}, timeout=0.1)
        except Exception as e:
            pytask.console.print_exception()


@pytask.hookimpl(tryfirst=True)
def pytask_execute_task_log_end(session: pytask.Session, report: pytask.ExecutionReport) -> None:
    
    try:    
        result = {'type': 'task', 'name' : report.task.short_name, 'outcome' : str(report.outcome)}
        res = requests.post('http://localhost:6000/pytask', json=result)
    except Exception as e:
        pytask.console.print_exception()
