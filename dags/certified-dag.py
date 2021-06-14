from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import get_current_context, PythonOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime, timedelta
from include import custom_function


DEFAULT_ARGS = dict(
    owner="airflow",
    depends_on_past=False,
    email_on_failure=False,
    email_on_retry=False,
    retries=1,
    retry_delay=timedelta(minutes=5),
)

DAG_ARGS = dict(
    start_date=datetime(2021, 6, 11),
    max_active_runs=3,
    schedule_interval="@daily",
    default_args=DEFAULT_ARGS,
    catchup=False,
)


@dag(**DAG_ARGS)
def certified_dag():
    t0 = DummyOperator(task_id="start")

    with TaskGroup("group_bash_tasks") as group_bash_tasks:
        bash_command = "sleep $[ ( $RANDOM % 30 )  + 1 ]s && date"
        t1 = BashOperator(
            task_id="bash_print_date1",
            bash_command=bash_command,
        )
        t2 = BashOperator(
            task_id="bash_print_date2",
            bash_command=bash_command,
        )

    for task_number in range(5):
        tn = task(task_id=f"python_print_date_{task_number}")(custom_function)(
            task_number=task_number
        )

        t0 >> tn

    t0 >> group_bash_tasks


dag = certified_dag()
