# AWS EC2 IP Updater for SSH Configuration

This script automatically updates the IP address of your EC2 instance in your SSH config file. This can be useful if your instance's IP address changes frequently (for example, when stopping and starting an EC2 instance).

<div align="center">
    <img src="https://showme.redstarplugin.com/s/x0VEGalE" />
</div>


* The user runs the update_ssh_config.sh script.
* The script fetches the new IP address of the EC2 instance using the AWS CLI.
* The AWS CLI returns the new IP address to the script.
* The script updates the SSH config file with the new IP address.

This process ensures that your SSH config file always has the current IP of your EC2 instance.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the AWS CLI on your machine. If not, follow the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
* You have configured the AWS CLI with your credentials. Run `aws configure` and follow the prompts to input your AWS Access Key ID, Secret Access Key, default region name, and default output format.

## Using AWS EC2 IP Updater

To use the script, follow these steps:

1. Save the following bash script in a file named `update_ssh_config.sh`, replacing `"your_instance_id_here"` with your actual EC2 instance ID:

    ```bash
    #!/bin/bash
    INSTANCE_ID="your_instance_id_here"

    # Get the new public IP address of the EC2 instance
    NEW_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

    # Define the config template
    read -r -d '' SSH_CONFIG << EOM
    Host short-name-of-your-choice
        HostName $NEW_IP
        User ubuntu
        IdentityFile path-to-.pem-file
        StrictHostKeyChecking no
    EOM

    # Write the new SSH config
    echo "$SSH_CONFIG" > ~/.ssh/config
    ```

2. Open a terminal and navigate to the directory where you saved the script:

    ```bash
    cd /path/to/directory
    ```

3. Make the script executable:

    ```bash
    chmod +x update_ssh_config.sh
    ```

4. Run the script:

    ```bash
    ./update_ssh_config.sh
    ```

This will update your SSH config file with the current IP of your EC2 instance.


[Previous](env-setup.md) | [Next](training.md)