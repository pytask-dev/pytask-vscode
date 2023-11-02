import pytask
import json
import requests
from contextlib import redirect_stdout
import io

@pytask.hookimpl(tryfirst=True)
def pytask_collect_log(session: pytask.Session, reports: list[pytask.CollectionReport], tasks: list[pytask.PTask]) -> None:
        try:    
            if session.config['command'] == 'collect':
                result = [{'name' : task.name.split('/')[-1], 'path' : str(task.path)} if isinstance(task,pytask.PTaskWithPath) else {'name' : task.name, 'path' : ''} for task in tasks]
                res = requests.post('http://localhost:6000/pytask', json={"exitcode" : session.exit_code, "tasks": result}, timeout=0.0001)
        except requests.exceptions.ReadTimeout: 
            pass
        except Exception as e:
            pytask.console.print_exception()


@pytask.hookimpl(tryfirst=True)
def pytask_execute_task_log_end(session: pytask.Session, report: pytask.ExecutionReport) -> None:
    
    try:
        if report.outcome == pytask.TaskOutcome.FAIL:
            with pytask.console.capture() as capture:
                pytask.console.print(pytask.render_exc_info(report.exc_info[0], report.exc_info[1], report.exc_info[2]))
            s = capture.get()
            result = {'type': 'task', 'name' : report.task.name.split('/')[-1], 'outcome' : str(report.outcome), 'exc_info' : s}
        else:
            result = {'type': 'task', 'name' : report.task.name.split('/')[-1], 'outcome' : str(report.outcome)}
        res = requests.post('http://localhost:6000/pytask', json=result, timeout=0.00001)
    except requests.exceptions.ReadTimeout: 
        pass
    except Exception as e:
        pytask.console.print_exception()
