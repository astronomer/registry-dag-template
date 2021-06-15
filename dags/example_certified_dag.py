from airflow.decorators import dag, task_group
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from datetime import datetime, timedelta
from include.example_custom_function import custom_function

# Default settings applied to all tasks within the DAG.
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

# Using the `@dag` decorator, the `dag` argument doesn't need to be specified for each
# task.  This functions the same way as the `with DAG()...` context manager.
@dag(**DAG_ARGS)
def certified_dag():
    t_start = DummyOperator(task_id="start")
    t_end = DummyOperator(task_id="end")

    with TaskGroup("group_bash_tasks") as group_bash_tasks:
        sleep = "sleep $[ ( $RANDOM % 30 )  + 1 ]s && date"

        t1 = BashOperator(
            task_id="bash_begin",
            bash_command="echo begin bash commands",
        )
        t2 = BashOperator(
            task_id="bash_print_date2",
            bash_command=sleep,
        )
        t3 = BashOperator(
            task_id="bash_print_date3",
            bash_command=sleep,
        )

        # Lists can be used to specify tasks to execute in parallel.
        t1 >> [t2, t3]

    t_start >> group_bash_tasks >> t_end

    # Generate tasks with a loop. The `task_id` must be unique across all tasks in a DAG.
    for task_number in range(5):
        tn = PythonOperator(
            task_id=f"python_print_date_{task_number}",
            python_callable=custom_function,
            op_kwargs=dict(task_number=task_number),
        )

        # When setting the dependencies, make sure they are indented inside the loop so
        # each task is added downstream of `t_start`.
        t_start >> tn >> t_end


dag = certified_dag()
