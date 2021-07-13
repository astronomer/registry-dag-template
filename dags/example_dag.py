from datetime import datetime, timedelta
from typing import Dict

from airflow.decorators import task
from airflow.models import DAG
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.weekday import BranchDayOfWeekOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.weekday import WeekDay


"""
This DAG is intended to be an example for community-provided DAGs.
"""

# Reference data for determining the activity to perform per day of week.
WEEKDAY_ACTIVITY_MAPPING = {
    "monday": "guitar lessons",
    "tuesday": "studying",
    "wednesday": "soccer practice",
    "thursday": "contributing to Airflow",
    "friday": "family dinner",
}


@task(multiple_outputs=True)
def going_to_the_beach() -> Dict[str, str]:
    return {
        "subject": "Beach day!",
        "body": "It's Saturday and I'm heading to the beach.<br><br>Come join me!<br>",
    }


# Using the DAG object as a context manager, the `dag` argument doesn't need to be specified
# for each task.
with DAG(
    dag_id="example_community_dag",
    start_date=datetime(2021, 6, 11),  # Best practice is to use a static start_date.
    max_active_runs=1,
    schedule_interval="@daily",
    # Default settings applied to all tasks within the DAG; can be overwritten at the task level.
    default_args={
        "owner": "community",
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
    },
    default_view="graph",
    catchup=False,
    tags=["example"],
) as dag:
    begin = DummyOperator(task_id="begin")
    end = DummyOperator(task_id="end", trigger_rule=TriggerRule.NONE_FAILED)

    check_day_of_week = BranchDayOfWeekOperator(
        task_id="check_day_of_week",
        week_day={WeekDay.SATURDAY, WeekDay.SUNDAY},
        follow_task_ids_if_true="weekend",
        follow_task_ids_if_false="weekday",
        use_task_execution_day=True,
    )

    weekend = DummyOperator(task_id="weekend")
    weekday = DummyOperator(task_id="weekday")

    # Templated value for determining the name of the day of week based on the execution date.
    day_name = "{{ execution_date.strftime('%A').lower() }}"

    # Begin weekday tasks.
    with TaskGroup("weekday_activities") as weekday_activities:
        which_weekday_activity_day = BranchPythonOperator(
            task_id="which_weekday_activity_day",
            python_callable=lambda day_name: f"weekday_activities.{day_name}",
            op_args=[day_name],
        )

        for day, activity in WEEKDAY_ACTIVITY_MAPPING.items():
            day_of_week = DummyOperator(task_id=day)
            do_activity = BashOperator(
                task_id=activity.replace(" ", "_"),
                bash_command=f"echo 'It's {day.capitalize()} and I'm busy with {activity}.'",
            )

            chain(which_weekday_activity_day, day_of_week, do_activity)

    # Begin weekend tasks.
    with TaskGroup("weekend_activities") as weekend_activities:
        which_weekend_activity_day = BranchPythonOperator(
            task_id="which_weekend_activity_day",
            python_callable=lambda day_name: f"weekend_activities.{day_name}",
            op_args=[day_name],
        )

        saturday = DummyOperator(task_id="saturday")
        sunday = DummyOperator(task_id="sunday")

        sleeping_in = BashOperator(
            task_id="sleeping_in", bash_command="sleep $[ ( $RANDOM % 30 )  + 1 ]s"
        )

        going_to_the_beach = going_to_the_beach()

        inviting_friends = EmailOperator(
            task_id="inviting_friends",
            to="friends@community.com",
            subject=going_to_the_beach["subject"],
            html_content=going_to_the_beach["body"],
        )

        chain(which_weekend_activity_day, [saturday, sunday])
        chain(saturday, going_to_the_beach, inviting_friends, end)
        chain(sunday, sleeping_in, end)

    # High-level dependencies.
    chain(begin, check_day_of_week, [weekday, weekend])
    chain(weekday, weekday_activities, end)
    chain(weekend, weekend_activities, end)

    # Task dependency created by XComArgs:
    #   going_to_the_beach >> inviting_friends
