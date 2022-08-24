<p align="center">
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" width="60" />
  </a>
</p>
<h1 align="center">
  Registry DAG Template
</h1>
  <h3 align="center">
  Guidelines on building, organizing, and publishing example DAGs for the Airflow community to discover and find inspiration from on the <a href="https://registry.astronomer.io/">Astronomer Registry</a>.
  </br></br>
  Maintained with ❤️ by Astronomer.
</h3>

</br>

<p align="center">
  For the best user experience by the Airflow community, example DAG repositories should be public on GitHub and follow the structural guidelines and practices presented below.
</p>

</br>

## Before you begin
An easy way to get started developing and running Apache Airflow pipelines locally is with the Astro CLI. Learn how to install it [here](https://docs.astronomer.io/astro/install-cli).  The CLI is also a great way to take advantage of this repository template.

</br>

## Repository structure
The organization of this repository resembles that generated by a project initialized by the Astro CLI. This template provides all the necessary files to run Apache Airflow locally within Docker containers using the Astro CLI along with an example DAG.
```bash
.
├── .astro
│   └── config.yaml # Configuration file for local environment settings
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── dags # DAG files go here
│   └── example_dag.py
├── packages.txt # For OS-level packages
└── requirements.txt # Place Provider packages as well as other Python modules used in your Airflow DAG here
```

Here are additional details about these files plus other directories and files that are optional to include in your own repository:

**`.astrocloud/config.yaml`**

   This file is used to establish settings to your local environment.  The `project.name` setting is declared in the file already to "registry_dag_template". Ideally this should be updated to a pertinent name for the project however.

**`Dockerfile`**

   The Dockerfile includes a reference to an Astronomer Certified Docker Image. Astronomer Certified (AC) is a Debian-based, production-ready distribution of Apache Airflow that mirrors the open source project and undergoes additional levels of rigorous testing conducted by the Astronomer team.

   This Docker image is hosted on [Astronomer's Docker Registry](https://quay.io/repository/astronomer/astro-runtime?tab=tags) and allows you to run Airflow on Astronomer. Additionally, the image you include in your Dockerfile dictates the version of Airflow you'd like to run locally.

   > **Note:** Airflow version 1.10.x reached end-of-life on June 17, 2021. It is strongly recommended to use a version of Airflow that is 2.0 or greater.

**`README.md`**

  The README for your example DAG repository has an understated importance -- it provides necessary context for the Airflow community about your DAG.  Feel free to include a use case description or a reason _why_ the DAG was created or even _how_ it can be used, the Airflow Providers used, the connections that are assumed to be in place to run the DAG, etc.  The more details, the better.

**`requirements.txt`**

  Any additional Python modules that are necessary to install in your local Airflow environment should be listed here.  This includes **Provider packages** which are used in the DAG.  For transparency of what versions of modules were used during development and testing of the DAG, **the versions should be pinned**.  This allows others to easily run, reproduce, and build upon the DAG while not having to guess what versions of modules were installed.

  For example:

    apache-airflow-providers-amazon==2.0.0
    apache-airflow-providers-salesforce==3.0.0
    apache-airflow-providers-snowflake==2.0.0
    jsonschema==3.2.0

  > Browse the Astronomer Registry to find all of the [available Providers](https://registry.astronomer.io/providers) that can be used in any Airflow DAG.

**`include/`** _[Optional]_

  This directory can be added as a main directory to the repository (i.e. same level as `dags/`) to house any other files.  This can be Python functions, small/reference datasets, custom Airflow `Operators`, SQL files, etc.  _With the Astro CLI, this directory is automatically read from so changes to any files in this directory will be picked up without having to restart your local environment._

  As part of a DAG-writing best practice, it is a good idea to separate accompanying logic and data from the logic which creates the `DAG`.  Think of the DAG file as a configuration file; it should be clean and ideally only contain logic for the `DAG` object, tasks, and task dependencies.  Using the `include/` directory can help improve organization of the repository greatly by providing a place to put the other "stuff".

  For example:

```bash
...
├── include
│   ├── operators
│   │   ├── __init__.py
│   │   └── custom_operator.py
│   └── sql
│   │   ├── extract
│   │   │   └── extract_data.sql
│   │   ├── load
│   │   │   └── insert_into_table.sql
│   │   └── transform
│   │       └── transform_other_data.sql
│   └── data
│       └── reference_data.csv
...
  ```

  > Before creating custom `Operators` or using the `PythonOperator` to execute logic, check out the Astronomer Registry to find all of the [available Modules](https://registry.astronomer.io/modules) that can be used out-of-the-box with Airflow Providers.

**`plugins/`** _[Optional]_

  This directory can be added as a main directory to the repository (i.e. same level as `dags/`) to house any logic for Airflow UI plugins like menu links.  _With the Astro CLI, this directory is automatically read from so changes to any files in this directory will be picked up without having to restart your local environment._

**`airflow_settings.yaml`** _[Optional]_

  When using the Astro CLI, this file can be used to programmatically create Connections, Variables, and Pools for your local Airflow environment.  For more information about this file, [check out this documentation](https://docs.astronomer.io/astro/develop-project/#configure-airflow_settingsyaml-local-development-only).

  > **Note:** Since this file can contain sensitive information like credentials, it is strongly recommended that this file be used for local development _only_ and not be published to GitHub.  The `.gitignore` within this repository template file does list the `airflow_settings.yaml` file so please do not remove the entry.

</br>

## Using this template
Follow the steps below to use the template and initialize a new repository locally.

1. Above the file list, click **Use this template**

    ![image](https://user-images.githubusercontent.com/48934154/122494828-a8a0b000-cfb7-11eb-8d51-5fb4aa47a32f.png)

2. Type a name for the repository, select **your user** as the owner, and an optional description.

    ![image](https://user-images.githubusercontent.com/48934154/125466191-28c50d72-927e-4da1-818b-01a4c43f1860.png)

3. Select **Public** visibility for the repository.

    ![image](https://user-images.githubusercontent.com/48934154/122496127-3f21a100-cfb9-11eb-8540-48f53c1b7d9c.png)

4. Click **Create repository from template**.

5. Clone the repository locally. Refer to the GitHub [documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) for different options of cloning repositories.

6. [Optional] Navigate to where the repository was cloned and run the following Astro CLI command to update the `project.name` setting in the `.astro/config.yaml` file provided in the repository.  This will update the name used to generate Docker containers and make them more discernible if there are multiple DAGs initialized locally via this template.

    ```bash
    astro config set project.name <name-of-repository>
    ```
7. To beginning development and testing of the DAG, run `astro dev start` to spin up a local Airflow environment. There is no need to run `astro dev init` as this functionality is already built in to the template repository.

</br>

## Publishing your DAG repository for the Astronomer Registry

Head over to the Astronomer Registry and [fill out the form](https://registry.astronomer.io/publish) with your shiny new DAG repo details!
