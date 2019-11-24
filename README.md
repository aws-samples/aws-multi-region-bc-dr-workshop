# Mythical Mysfits: Building Multi-Region Applications that Align with BC/DR Objectives

## Overview
![mysfits-welcome](/images/mysfits-welcome.png)

**Mythical Mysfits** is a (fictional) pet adoption non-profit dedicated to helping abandoned, and often misunderstood, mythical creatures find a new forever family! Mythical Mysfits believes that all creatures deserve a second chance, even if they spent their first chance hiding under bridges and unapologetically robbing helpless travelers.

Our business has been thriving with only a single Mysfits adoption center, located inside Devils Tower National Monument. Speak, friend, and enter should you ever come to visit.

We've just had a surge of new mysfits arrive at our door with nowhere else to go!  They're all pretty distraught after not only being driven from their homes... but an immensely grumpy ogre has also denied them all entry at a swamp they've used for refuge in the past.  

That's why we've hired you to be our first Full Stack Engineer. We need a more scalable way to show off our inventory of mysfits and let families adopt them. We'd like you to build the first Mythical Mysfits adoption website to help introduce these lovable, magical, often mischievous creatures to the world!

We're growing, but we're struggling to keep up with our new mysfits mainly due to our legacy inventory platform.  We have already moved to containers, but have a lack of observability and we are starting up contracts with companies that require us to be up all the time.

### Requirements:
* AWS account - if you don't have one, it's easy and free to [create one](https://aws.amazon.com/)
* AWS IAM account with elevated privileges allowing you to interact with CloudFormation, IAM, EC2, ECS, ECR, ALB, VPC, SNS, CloudWatch, AWS CodeCommit, AWS CodeBuild, AWS CodePipeline
* Familiarity with Python, vim/emacs/nano, [Docker](https://www.docker.com/), AWS and microservices - not required but a bonus

### What you'll do:

These labs are designed to be completed in sequence, and the full set of instructions are documented below.  Read and follow along to complete the labs.  If you're at a live AWS event, the workshop attendants will give you a high level run down of the labs and help answer any questions.  Don't worry if you get stuck, we provide hints along the way.  

* **[Lab 0](lab-0-init):** Deploy Existing Mythical Stack
* **[Lab 1](lab-1-xray):** Get Operational Visibility via X-ray and Custom Metrics
* **[Lab 2](lab-2-agg):** Build Operational Dashboard
* **[Lab 3](lab-3-mr-prep):** Prep your app for multi-region deployment
* **[Lab 4](lab-4-globalacc):** Implement Global Accelerator and manual failover
* **[Lab 5](lab-5-loadtest):** Load test the system, test your metrics, manual failover
* **[Bonus Lab](/):** [DOES NOT EXIST YET] Bonus lab for something or other
* **Workshop Cleanup** [Cleanup working environment](#workshop-cleanup)

### Conventions:
Throughout this workshop, we will provide commands for you to run in the terminal.  These commands will look like this:

<pre>
$ ssh -i <b><i>PRIVATE_KEY.PEM</i></b> ec2-user@<b><i>EC2_PUBLIC_DNS_NAME</i></b>
</pre>

The command starts after the $.  Text that is ***UPPER_ITALIC_BOLD*** indicates a value that is unique to your environment.  For example, the ***PRIVATE\_KEY.PEM*** refers to the private key of an SSH key pair that you've created, and the ***EC2\_PUBLIC\_DNS\_NAME*** is a value that is specific to an EC2 instance launched in your account.  You can find these unique values either in the CloudFormation outputs or by going to the specific service dashboard in the [AWS management console](https://console.aws.amazon.com).

If you are asked to enter a specific value in a text field, the value will look like `VALUE`.

Hints are also provided along the way and will look like this:

<details>
<summary>HINT</summary>

**Nice work, you just revealed a hint!**
</details>


*Click on the arrow to show the contents of the hint.*

### IMPORTANT: Workshop Cleanup

You will be deploying infrastructure on AWS which will have an associated cost. If you're attending an AWS event, credits will be provided.  When you're done with the workshop, [follow the steps at the very end of the instructions](#workshop-cleanup) to make sure everything is cleaned up and avoid unnecessary charges.

* * *

## Let's Begin!

[Go to Lab-0 to set up your environment](lab-0-init)

### Workshop Cleanup

This is really important because if you leave stuff running in your account, it will continue to generate charges.  Certain things were created by CloudFormation and certain things were created manually throughout the workshop.  Follow the steps below to make sure you clean up properly.  

1. Delete any manually created resources throughout the labs, e.g. CodePipeline Pipelines and CodeBuild projects.  Certain things like task definitions do not have a cost associated, so you don't have to worry about that.  If you're not sure what has a cost, you can always look it up on our website.  All of our pricing is publicly available, or feel free to ask one of the workshop attendants when you're done.
2. Go to the CodePipeline console and delete prod-like-service. Hit Edit and then Delete.
3. Delete any container images stored in ECR, delete CloudWatch logs groups, and empty/delete S3 buckets
4. In your ECS Cluster, edit all services to have 0 tasks and delete all services
5. Delete log groups in CloudWatch Logs
6. Finally, delete the CloudFormation stack launched at the beginning of the workshop to clean up the rest.  If the stack deletion process encountered errors, look at the Events tab in the CloudFormation dashboard, and you'll see what steps failed.  It might just be a case where you need to clean up a manually created asset that is tied to a resource goverened by CloudFormation.

