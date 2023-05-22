# Maturity model

<div align="center">
    <img src="https://kroki.io/mermaid/svg/eNqVUV1v2kAQfO-vWJFXI_AHJbhSpQSolAqaSKRPUR8OezFXH3fW3TqJpfz4rs84kL60PN7M7M3uTGFFtYfH208AGxKWngbr1X3lYC2otpKawS9mVuOnwQqfUcE4hR8GvKRjwp4JU1jgczu6rQn0B1HUi6IUbmoyB0GYw6MVUktddJq418TnmgVWyjQH1NSpkl6VpPCtVqpz6Qek0V7mL4Hh8OvbgLcV72QANzySmRxBavheVw2h5V0Jt8aULoBNLUlsFcLOWHi4n0NlzW_MyA3eOASfRPftaUOLCoVDHp7fjeaLAH5qSaM7TVhYbwqEjpheCBKwySTfIhkAoXNY6kJqROvgxdgSHFaCh1A1rV_o8_3bj46pQSUrVDwdwPK1QivbkFo2K5kNYM1XKt6uYDPb_Jc9mQJpj7Y1j3xvnflSuAYO_r_8vQ_OcnTrbzuzOxg-3th2PQ64UiLD9rPYF9x91rbW9J2c39MudP79gxVFW5s7gHRQos8k4Z8cNdwQN7GTSqVXu1k-wckJD484oshmsxMe9fj4czydnvD4iGfXcZyc6ZMjPtnG08k14xx2ufHcmDXWlJheRZjl0zDonsMXmdM-jarXLx_k4WXy6DJ5fJk8-bf8D8qaVqQ" />
</div>

* Level 0: No MLOps - No automation, all code is in Jupyter notebooks. This level is suitable for Proof of Concept (POC) projects.
* Level 1: DevOps but no MLOps - Releases are automated, there are unit and integration tests, CI/CD is in place. However, data scientists and engineers work separately.
* Level 2: Automated Training - There is an automated training pipeline, experiment tracking, and a model registry. Data scientists and engineers work together in this stage.
* Level 3: Automated Deployment - It's easy to deploy models, there are A/B tests, and model monitoring is in place.
* Level 4: Full MLOps Automation - Training and deployment are fully automated. Pragmatism is key at this level.

[Previous](best-practices.md)