def custom_function(task_number, **kwargs):
    """
    This can be any Python code you want and is called from the `PythonOperator`.
    The code is not executed until the task is run by the Airflow Scheduler.
    """

    context = get_current_context()
    print(
        f"I am task number {task_number}."
        f"This DAG Run execution date is {context['ts']} and the current time is {datetime.now()}"
    )
    print(f"Here is the full DAG Run context: {context}")
