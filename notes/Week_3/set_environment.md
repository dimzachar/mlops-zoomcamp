# Chapter 2: Understanding Prefect and its Components

This chapter thoroughly introduces Prefect, its components, and relevant terminology. 

It covers the process of configuring a local database, elucidating key steps such as setting up tables, establishing connections, and handling data. 

It explores the setup of the Prefect environment and running scripts on the Prefect server. 

## Setting Up Your Environment for Prefect 2.0

Before you can start using Prefect 2.0, you'll need to set up your environment. This involves installing Prefect and its dependencies. Here's how you can do it:

- **Install Prefect:** Prefect is a Python package, and you can install it using pip. Open a terminal and run the following command:

```
pip install prefect
```

- **Set Up a Virtual Environment (Optional):** It's a good practice to create a virtual environment for your Python projects. This keeps the dependencies for each of your projects separate, reducing the risk of version conflicts.

- **Install Additional Dependencies:** If your workflows require additional Python packages, you can install them in the same way

```
pip install -r requirements.txt
```

- **Verify Your Installation:** You can check that Prefect is installed correctly by running the following command:

```
prefect --version
```

This should print the version of Prefect that you installed.

- **Start the Prefect Server:** You can start the Prefect server by running the following command:

```
prefect server start
```


Now that your environment is set up, you're ready to start creating workflows with Prefect 2.0!

[Previous](intro.md) | [Next](workflow.md)