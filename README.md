# Mythical Mysfits: Building Multi-Region Applications that Align with BC/DR Objectives

![mysfits-welcome](../images/mysfits-welcome.png)

## Overview
![mysfits-welcome](/images/mysfits-welcome.png)

**Mythical Mysfits** is a (fictional) pet adoption non-profit dedicated to helping abandoned, and often misunderstood, mythical creatures find a new forever family! Mythical Mysfits believes that all creatures deserve a second chance, even if they spent their first chance hiding under bridges and unapologetically robbing helpless travelers.

Our first adoption agency, founded in Devils Tower National Monument, has helped millions of mythical mysfits find loving homes. Since then, we've deployed expedition teams to far reaching corners of the Earth to seek out more wandering communities of mythical mysfits in need of care and hugs. Initial reports indicate that we'll need to expand our operation globally.

To support our global expansion, we're doubling down on our digital adoption experience and have formed a team to re-architect for multi-region expansion. The initial goal is to enable a secondary region for disaster recovery (DR) purposes, which is a part of our business continuity planning. We could have built out DR in a single AWS region by leveraging multiple AZs, but we need to account for regional level disasters since mysfit lives are on the line. Our partners also emphasize in their contracts with us that we must maintain high degrees of availability. Lastly, this will set us up nicely for multi-region active-active as we open new adoption centers around the world.

To recap our progress to date, we've modernized our stack to be containerized microservices deployed with AWS Fargate. We manage our resources using infrastructure as code and have a fully automated CI/CD pipeline that deploys our code changes. Our solution architects have drafted a DR plan that leverages a secondary region. We need your help to carry out this plan by first improving observability, so we can make data driven decisions for things like regional failover. Then we'll need help with data replication, multi-region builds, and traffic management. Can you help us out?

### Requirements

* AWS account - if you're doing this workshop as a part of an AWS event, you will be provided an account through a platform called Event Engine. The workshop administrator will provide instructions. If the event specifies you'll need your own account or if you're doing this workshop on your own, it's easy and free to [create an account](https://aws.amazon.com/) if you do not have one already.
* If using your own AWS account, create and use an IAM account with elevated privileges. Easiest option is to create an IAM user with admin privileges.

Familiarity with AWS, Python, [Docker](https://www.docker.com/), networking, CI/CD, and git is a plus but not required.

### What you'll do

The labs in the workshop are designed to be completed in sequence, and the full set of instructions are documented in each lab. Read and follow the instructions to complete each of the labs. Don't worry if you get stuck, we provide hints along the way.

* **[Lab 0](lab-0-init):** Deploy existing Mythical stack
* **[Lab 1](lab-1-xray):** Improve microservices observability with distributed tracing
* **[Lab 2](lab-2-agg):** Build an operational dashboard
* **[Lab 3](lab-3-mr-prep):** Prepare the app for multi-region deployments
* **[Lab 4](lab-4-globalacc):** Implement AWS Global Accelerator and test traffic management
* **[Lab 5](lab-5-loadtest):** Load test the system to test manual failover based on operational metrics
* **[Bonus Lab](/):** [DOES NOT EXIST YET] Implement automated failover and active-active
* **Workshop Cleanup** [Cleanup working environment](#important-workshop-cleanup)

### Conventions

#### 1. Commands

Throughout this workshop, we will provide commands for you to run in a terminal. These commands will look like this:

<pre>
$ ssh -i <b><i>PRIVATE_KEY.PEM</i></b> ec2-user@<b><i>EC2_PUBLIC_DNS_NAME</i></b>
</pre>

The command starts **after** the $.

#### 2. Unique values

If you see ***UPPER_ITALIC_BOLD*** text, that means you need to enter a value unique to your environment. For example, the ***PRIVATE\_KEY.PEM*** above refers to the private key of an SSH key pair that's specific to your account; similarly, the ***EC2_PUBLIC_DNS_NAME*** refers to the DNS name of an EC2 instance in your account.

All unique values required throughout the workshop are captured as outputs from the CloudFormation template you'll launch to set up the workshop environment. You can, of course, also visit the specific service's dashboard in the [AWS management console](https://console.aws.amazon.com).

#### 3. Specific values or text

If you are asked to enter a specific value or text, it will formatted like this - `verbatim`.

#### 4. Hints

Hints are also provided along the way and will look like this:

<details>
<summary>HINT</summary>

**Nice work, you just revealed a hint!**
</details>

*Click on the arrow to show the contents of the hint.*

### IMPORTANT: Workshop Cleanup

If you're attending an AWS event and are provided an account to use, you can ignore this section because we'll destroy the account once the workshop concludes. Feel free to proceed to [Lab-0 to get started](lab-0-init).

**If you are using your own account**, it is **VERY** important you clean up resources created during the workshop. Follow these steps to delete the main workshop CloudFormation stack once you're done going through the workshop:

1. Navigate to the [CloudFormation dashboard](https://console.aws.amazon.com/cloudformation/home#/stacks) and click on your workshop stack name to load stack details
2. Click **Delete** to delete the stack

There are helper Lambda functions that should clean things up when you delete the main stack. However, if there's a stack deletion failure due to a race condition, follow these steps:

1. In the CloudFormation dashboard, click on the **Events** section, and review the event stream to see what failed to delete
2. Manually delete those resources by visiting the respective service's dashboard in the management console
3. Once you've manually deleted the resources, try to delete the main workshop CloudFormation stack again. Repeat steps 1-3 if you still see deletion failures

* * *

## Let's Begin!

[Go to Lab-0 to set up your environment](lab-0-init)
