from airflow.decorators import dag, task, task_group
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta


"""
This DAG is intended to be an example of what a Certified DAG could look like. It is
based on the `example-dag.py` file that is included with projects initialized with the
`astro dev init` Astro CLI command.
"""

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

    @task_group
    def group_bash_tasks(command) -> None:
        t1 = BashOperator(
            task_id="bash_begin",
            bash_command="echo begin bash commands",
        )
        t2 = BashOperator(
            task_id="bash_print_date2",
            bash_command=command,
        )
        t3 = BashOperator(
            task_id="bash_print_date3",
            bash_command=command,
        )

        # Lists can be used to specify tasks to execute in parallel.
        t_start >> t1 >> [t2, t3] >> t_end

    sleep = "sleep $[ ( $RANDOM % 30 )  + 1 ]s && date"
    group_bash_tasks(command=sleep)

    # Generate tasks with a loop.
    for task_number in range(5):
        # The `task_id` must be unique across all tasks in a DAG.
        @task(task_id=f"python_print_date_{task_number}")
        def custom_function(task_number: int, **context) -> None:
            """
            This can be any Python code you want and is called in a similar manner to
            the `PythonOperator`. The code is not executed until the task is run by the
            Airflow Scheduler.
            """

            print(
                f"I am task number {task_number}. "
                f"This DAG Run execution date is {context['ts']} and the current time is {datetime.now()}."
            )
            print(f"Here is the full DAG Run context: {context}")

        # When setting the dependencies, make sure they are indented inside the loop so
        # each task is added downstream of `t_start`.
        t_start >> custom_function(task_number) >> t_end


dag = certified_dag()
