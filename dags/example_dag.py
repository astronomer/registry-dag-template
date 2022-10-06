"""
This will be the DAG display title on the Astronomer Registry

This DAG is intended to be a demonstration of a number of core Airflow concepts related to pipeline authoring
including TaskFlow API, branching, Edge Labels, Jinja templating, dynamic task generation, Task Groups, and
Trigger Rules.
"""

from datetime import timedelta
from pendulum import datetime
from typing import Dict

from airflow.decorators import dag, task, task_group
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.weekday import BranchDayOfWeekOperator
from airflow.utils.edgemodifier import Label
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.weekday import WeekDay


# Reference data for determining the activity to perform per day of week.
DAY_ACTIVITY_MAPPING = {
    "monday": {"is_weekday": True, "activity": "guitar lessons"},
    "tuesday": {"is_weekday": True, "activity": "studying"},
    "wednesday": {"is_weekday": True, "activity": "soccer practice"},
    "thursday": {"is_weekday": True, "activity": "contributing to Airflow"},
    "friday": {"is_weekday": True, "activity": "family dinner"},
    "saturday": {"is_weekday": False, "activity": "going to the beach"},
    "sunday": {"is_weekday": False, "activity": "sleeping in"},
}


@task(multiple_outputs=True)
def going_to_the_beach() -> Dict:
    return {
        "subject": "Beach day!",
        "body": "It's Saturday and I'm heading to the beach.<br><br>Come join me!<br>",
    }


@task.branch()
def get_activity(day_name: str) -> str:
    activity_id = DAY_ACTIVITY_MAPPING[day_name]["activity"].replace(" ", "_")

    if DAY_ACTIVITY_MAPPING[day_name]["is_weekday"]:
        return f"weekday_activities.{activity_id}"

    return f"weekend_activities.{activity_id}"


@task_group()
def weekday_activities(day_name: str) -> None:
    which_weekday_activity_day = get_activity.override(task_id="which_weekday_activity_day")(
        day_name=day_name
    )

    for day, day_info in DAY_ACTIVITY_MAPPING.items():
        if day_info["is_weekday"]:
            day_of_week = Label(label=day)
            activity = day_info["activity"]

            do_activity = BashOperator(
                task_id=activity.replace(" ", "_"),
                bash_command=f"echo It's {day.capitalize()} and I'm busy with {activity}.",
            )

            # Declaring task dependencies within the `TaskGroup` via the classic bitshift operator.
            chain(which_weekday_activity_day, day_of_week, do_activity)


@task_group()
def weekend_activities(day_name: str) -> None:
    which_weekend_activity_day = get_activity.override(task_id="which_weekend_activity_day")(
        day_name=day_name
    )

    saturday = Label(label="saturday")
    sunday = Label(label="sunday")

    sleeping_in = BashOperator(task_id="sleeping_in", bash_command="sleep $[ ( $RANDOM % 30 )  + 1 ]s")

    beach_time = going_to_the_beach()

    # Because the ``going_to_the_beach()`` function has ``multiple_outputs`` enabled, each dict key is
    # accessible as their own `XCom` key.
    EmailOperator(
        task_id="inviting_friends",
        to="friends@community.com",
        subject=beach_time["subject"],
        html_content=beach_time["body"],
    )

    # Using ``chain()`` here for list-to-list dependencies which are not supported by the bitshift
    # operator and to simplify the notation for the desired dependency structure.
    chain(which_weekend_activity_day, [saturday, sunday], [beach_time, sleeping_in])

    # Task dependency created by XComArgs:
    #   going_to_the_beach >> inviting_friends


# When using the DAG decorator, the ``dag`` argument doesn't need to be specified for each task.
# The ``dag_id`` value defaults to the name of the function it is decorating.
@dag(
    start_date=datetime(2021, 6, 11),  # Best practice is to use a static start_date.
    max_active_runs=1,
    schedule_interval="@daily",
    # Default settings applied to all tasks within the DAG; can be overwritten at the task level.
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
    },
    default_view="graph",
    catchup=False,
    tags=["example"],
    doc_md=__doc__,
)
def example_registry_dag():
    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.NONE_FAILED)

    check_day_of_week = BranchDayOfWeekOperator(
        task_id="check_day_of_week",
        week_day={WeekDay.SATURDAY, WeekDay.SUNDAY},
        follow_task_ids_if_true="weekend",
        follow_task_ids_if_false="weekday",
        use_task_execution_day=True,
    )

    weekend = EmptyOperator(task_id="weekend")
    weekday = EmptyOperator(task_id="weekday")

    # Templated value for determining the name of the day of week based on the start date of the DagRun.
    day_name = "{{ dag_run.start_date.strftime('%A').lower() }}"

    # Begin weekday tasks.
    weekday_tasks = weekday_activities(day_name=day_name)

    # Begin weekend tasks
    weekend_tasks = weekend_activities(day_name=day_name)

    # High-level dependencies.
    chain(begin, check_day_of_week, [weekday, weekend], [weekday_tasks, weekend_tasks], end)


example_registry_dag()
