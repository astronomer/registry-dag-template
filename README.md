<p align="center">
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" width="60" />
  </a>
</p>
<h1 align="center">
  Astronomer Registry DAG Template Repository
</h1>
  <h3 align="center">
  Guidelines on building, organizing, and publishing example DAGs for the Airflow community to discover, find inspiration from, and utilize. Maintained with ❤️ by Astronomer.
</h3>
  

Follow the steps below to use the template and initialize a new repository locally.

1. Above the file list, click **Use this template**

![image](https://user-images.githubusercontent.com/48934154/122494828-a8a0b000-cfb7-11eb-8d51-5fb4aa47a32f.png)

2. Type a name for the repository, and an optional description.

![image](https://user-images.githubusercontent.com/48934154/122496102-35983900-cfb9-11eb-8074-ccd5b9529d8d.png)

3. Select **Public** visibility for the repository.

![image](https://user-images.githubusercontent.com/48934154/122496127-3f21a100-cfb9-11eb-8540-48f53c1b7d9c.png)

4. Click **Create repository from template**.

5. Clone the repository locally. Refer to the GitHub [documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) for different options of cloning repositories.

6. [Optional] Navigate to where the repository was cloned and run the following Astro CLI command to update the project.name setting in the .astro/config.yaml file provided in the repository.  This will update the name used to generate Docker containers and make them more discernible if there are multiple Certified DAGs initialized locally. 
```bash
astro config set project.name <name of repository>
```
7. To beginning development and testing of the DAG, run `astro dev start` to spin up a local Airflow environment. There is no need to run `astro dev init` as this functionality is already built in to the template repository.
