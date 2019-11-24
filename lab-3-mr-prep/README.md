# Mythical Mysfits: Multi-Region-Workshop

## Lab 3 - Preparing for multi-region deployments
<!-- **steve has slides on this - things u may have forgotten** - it's in chat -->

In this section, you will begin preparations for moving your application to multiple regions. It's very common to forget a number of steps along the way as many people will mainly think of infrastructure and the application itself to move over, but there are a number of assets that also need to be referenced.

These are the things that we will need to replicate and also automate:
* Infrastructure
  * Network
  * Docker Repositories
  * ECS
* Container images
* Application Deployments

<!-- Here's a reference architecture for what you'll be building:

[TODO] CREATE REF ARCHITECTURE PICTURE
![CodeBuild Create](images/arch-codebuild.png)

Here's what you'll be doing:

[TODO] CREATE TOC
* [Create AWS CodeBuild Project](#create-aws-codebuild-project)
* [Create BuildSpec File](#create-buildspec-file)
* [Test your AWS CodeBuild Project](#test-your-aws-codebuild-project) -->

### Infrastructure Replication
At the beginning of the workshop, you used AWS CloudFormation to create the infrastructure. We'll do the same thing now to replicate it, but we'll enter in a different parameter.

First we will replicate the main infrastructure using a new CloudFormation stack. Note that there are a bunch of different ways to do this, like updating a CodePipeline pipeline to deploy to another region or using stacksets. We just make it a bit simpler by running this manually.

<pre>
$ cd ~/environment/multi-region-workshop
$ aws cloudformation deploy --stack-name mm-secondary-region --template-file cfn/core.yml --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --parameter-overrides IsDrRegion=true --region us-east-1
</pre>

Once it says CREATE_COMPLETE, navigate to the Outputs tab of the stack. Note the values of:
* SecondaryLikeServiceEcrRepo
* SecondaryMythicalServiceEcrRepo
* SecondaryLoadBalancerDNS

### Database Replication

The most difficult part of a multi-region application is typically data synchronization. Now that you have a separate stack, we need to set up DynamoDB so that it automatically replicates any data created using the app in the primary region.

There's an easy way to do this - DynamoDB Global Tables. This feature will ensure we always have a copy of our data in both our primary and failover region by continuously replicating changes using DynamoDB Streams. We'll set this up now.

## Given this was only released recently, these instructions are quick and dirty (for now).
[TODO - Add screenshots]

In your source region (double check this) DynamoDB, select the table. It will be named 'MythicalMysfits-DDB-\*' followed by your chosen stack name.

![Configure DynamoDB with Global Tables](../images/03-ddb-global-tables-screen.png_DELIBERATEBREAK)

Next, choose the Global Tables tab from the top, click **Enable Streams**. Once Streams have been enabled, under **Global Table Regions**, click Add region and add the US-East region and click Create replica. (This will take about 5 minutes so proceed with the rest of this lab and it'll work away in the background).

![Configure DynamoDB with Global Tables](images/03-ddb-create-gt.png_DELIBERATEBREAK)

Take a look at DynamoDB in your **Primary Region** and also in your **Secondary Region**. You should see that the objects have already been propagated.

### Deployment Replication

Now that you have all your artifacts replicated into the secondary region, you can automate the deployments too. The CICD infrastructure is already provisioned for you. To automate the deployments into the secondary region, we'll use [AWS CodePipeline's Cross-Region Actions](https://aws.amazon.com/about-aws/whats-new/2018/11/aws-codepipeline-now-supports-cross-region-actions/).

Navigate to the [CodePipeline console](http://console.aws.amazon.com/codepipeline) of the **PRIMARY** region. Click on the pipeline that starts with *Core*. Note that if your pipelines are not in a **Succeeded** state, there was a problem. Try to get your deployments into a **Succeeded** state before proceeding. You may have to re-run some setup scripts.

![Select Core Pipeline](images/03-codepipeline-core.png)

Click on **Edit** and **Add stage** after the Deploy stage.

![Edit Core {Pipeline}](images/03-codepipeline-edit.png)

Type in **CrossRegionDeploy** for the stage name.

![Edit Core {Pipeline}](images/03-codepipeline-cross-region-deploy.png)

Next we will configure the stage so that it deploys to ECS in the secondary region. In the new CrossRegionDeploy stage, click **Add Action Group**. Enter in the following details in the **Edit Action** popup:

**Edit Action**:
* Click on **Add Action Group** and enter the following details:
* Action name: **CrossRegionDeploy**
* Action provider: **Amazon ECS**
* Region: **Choose the secondary region you deployed into** - By default, this should be US East - (N. Virginia)
* Input artifacts: **BuildArtifact**
* Cluster name: **Choose the cluster that was created for you. It will start with Cluster-**
* Service name: **Select the service that includes "Core"**
* Image definitions file: **imagedefinitions_secondary.json** - The value of this will depend on what you output in your buildspec. Our default is imagedefinitions_secondary.json.

![Create Action](images/03-cp-createactiongroup.png)

Click **Done** and then **Save** at the top of the screen. Click through prompts until you're back at the pipeline. At this point, you should see your pipeline again and the final stage will be grey because it has not run yet.

**Do this again for the Like Service**

![Do it again](images/03-codepipeline-like.png)

**Edit Action**:
* Click on **Add Action Group** and enter the following details:
* Action name: **CrossRegionDeploy**
* Action provider: **Amazon ECS**
* Region: **Choose the secondary region you deployed into** - By default, this should be US East - (N. Virginia)
* Input artifacts: **BuildArtifact**
* Cluster name: **Choose the cluster that was created for you. It will start with Cluster-**
* Service name: **Select the service that includes "Like"**
* Image definitions file: **imagedefinitions_secondary.json** - The value of this will depend on what you output in your buildspec. Our default is imagedefinitions_secondary.json.

![Do it again with the like](images/03-cp-createactiongroup-like.png)

### Update build scripts to upload docker images to both regions

As part of the infrastructure automation, we gave you the application for both **core** and **like** services. You will now have to manually update the buildspec_prod.yml file to upload the container image to another region.

First, we will update the `core-service` app. Navigate to the core-service codecommit repo. You can do this in the side navigation pane or via CLI.

Console:
![Find file on nav pane](images/03-core-service_buildspec.png)

CLI:
<pre>
  $ cd ~/environment/core-service-[PRESS TAB TO AUTO COMPLETE AND PRESS ENTER]
</pre>

Find the buildspec_prod file in both mysfits-service and like-service. Update them to push your conainers and application to both regions. Within both of the buildspecs there are [TODO] lines to guide you through what you'll need to do. It's your choice if you want to understand how the build process works. Otherwise...

[TODO:] mod bootstrap to change these buildspecs

<details>
<summary>Click here for a completed buildspec and commands to copy them in:</summary>
We have created some completed buildspec files if you want to skip this portion. They are in the app/hints folder.
<pre>
  $ cd ~/environment/core-service-[PRESS TAB TO AUTO COMPLETE AND PRESS ENTER]
  $ cp ~/environment/multi-region-workshop/app/hints/mysfits-service-buildspec_prod.yml buildspec_prod.yml
  $ cd ~/environment/like-service-[PRESS TAB TO AUTO COMPLETE AND PRESS ENTER]
  $ cp ~/environment/multi-region-workshop/app/hints/like-buildspec_prod.yml buildspec_prod.yml

Open the two files and replace these variables:
* REPLACEME_SECONDARY_REGION with your secondary region (default **us-east-1**) in both buildspec_prod.yml files
* REPLACEME_CORE_REPOURI_SECONDARY with the value of **SecondaryMythicalServiceEcrRepo** from the Cloudformation outputs in the Core service buildspec_prod.yml
* REPLACEME_LIKE_REPOURI_SECONDARY with the value of **SecondaryLikeServiceEcrRepo** from the CloudFormation outputs in the Like service buildspec_prod.yml

*Note that in these labs we are hard coding values, but best practice is to use environment variables instead. This just simplifies the process for illustrative purposes.*
</pre>
</details>

<details>
<summary> Click here for a script that will do it for you</summary>
<pre>
[TODO] Haven't done this yet. Would have to get the region and then get the stack and then the outpots
</pre>
</details>

### Trigger deployment again

Finally, add all the files to both repos and trigger deployments:

<pre>
  $ cd ~/environment/<b>core-service-[PRESS TAB TO AUTO COMPLETE AND PRESS ENTER]</b>
  $ git add -A
  $ git commit -m "Updating core buildspec for multi-region deploy"
  $ git push origin master
  $ cd ~/environment/<b>like-service-[PRESS TAB TO AUTO COMPLETE AND PRESS ENTER]</b>
  $ git add -A
  $ git commit -m "Updating like buildspec for multi-region deploy"
  $ git push origin master
</pre>

### Enabling Cloudwatch Dashboard to show multi-region metrics

Now that you have deployed the stack in the secondary region, lets adjust the Cloudwatch dashboard that you created in the previous lab to include these new resources. This will provide visibility to the Mythical and Like services running across both regions on the same dashboard.

If you are unfamiliar with Amazon Cloudwatch, you may consider creating a duplicate of the current Cloudwatch dashboard for safe keeping. That way you can always revert back to the original if you need to.

<details>
    <summary>Instructions: How do I do this?</summary>

* Select the Cloudwatch dashboard you wish to duplicate
* Click **Actions** followed by **Save dashboard as...**
* Enter a name for the new dashboard - **BackupOfMyDashboard**
* Click **Save dashboard**

</details>


### X. Edit the widgets to show metrics from the other region

With Amazon Cloudwatch, we have the ability to stack metrics on top of each other in a widget that contains a graph. This will be useful in our case where we are viewing the same metric type, over two resources. We'll do this in the steps below in addition to adding the metrics from the other region.

Hint - see documentation for [Editing a Graph on a Cloudwatch Dashboard](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/edit_graph_dashboard.html)

### X.a Edit the ALB widgets

As we are now adding in metrics from two different regions, we must navigate to the secondary region and load the dashboard from there. This is because when referring to metrics within a dashboard, Cloudwatch can only see resources local to that region.

Modify the ALB Requests Per Minute widget to show the metrics from the ALB in the secondary region:

* Open up the [Cloudwatch Dashboards](https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#dashboards:) page and select the dashboard you created in the previous lab
* Change the region (top right of screen) to your Secondary region
* Change the widget to a stacked area
* Add in the **RequestCount** metric to this widget from the ALB
* Change the metric labels to identify the correct region for that metric

<details>
    <summary>Hint with screenshots:</summary>

* Hover over the widget and select Edit in the top right hand corner
![image](https://user-images.githubusercontent.com/23423809/69213104-03420380-0b18-11ea-8cff-e25b09c70fb5.png)
* Change the graph type from a Line to Stacked Area. Then select the All Metrics tab and add in the **requestcount** metric from the ALB
![image](https://user-images.githubusercontent.com/23423809/69213968-83696880-0b1a-11ea-9d71-18a2c1dbfd62.png)
* Select Graphed Metrics and change the label to match the region
![image](https://user-images.githubusercontent.com/23423809/69214232-2d48f500-0b1b-11ea-83a4-2ae1e7dfeade.png)
* Click **Update widget**
    </details>

Modify the ALB HTTP Responses widget to show the metrics from the ALB in the secondary region:

* Change the widget to a stacked area
* Add in the **HTTP 2XX / 4XX / 5XX Count** metrics from the ALB
* Change the metric labels to identify the correct region for that metric
* Ensure the region you put in the label matches the region in the details
* Click **Update widget**

<details>
<summary>Show screenshot:</summary>

![image](https://user-images.githubusercontent.com/23423809/69214680-7188c500-0b1c-11ea-8a81-cdb1d549dfb9.png)

</details>


### X.b Add widgets for the Like and Mythical Services from Secondary region

Following the same process from Lab 2, add a new widget for each of the Like and Mytical services. Modify the titles to be able to easily identify which region they are populating from. You should end up with something like this:

![image](https://user-images.githubusercontent.com/23423809/69214987-46eb3c00-0b1d-11ea-8317-94c55dad4af2.png)

Feel free to move the widgets around the dashboard to suit your style following the instructions in the [https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/move_resize_graph_dashboard.html](Cloudwatch documentation).
Youc can drag widgets around and move them into position wherever you like. You can also add a text widget to show a title, include links to a knowledgebase wiki or internal tooling. Get creative!

[TODO - Add Andy's KPIs / other metrics from X-Ray]

### X.c Add a widget to show statistics from the DynamoDB Global Table

While we're at it, lets create a new widget showing the the Read Capacity Units and Write Capacity Units for our newly created Global Table. Monitoring the table ensures that we have full visibility of the amount of read and write activity which can be useful in troubleshooting efforts.

Here's how:

* Create a new stacked area graph on the Cloudwatch Dashboard
* Select **DynamoDB**, **Table Metrics**, **[insert table name]**, **ConsumedReadCapacityUnits** and **ConsumedWriteCapacityUnits**
**ConsumedWriteCapacityUnits** for our DynamoDB Global Table.
* Change the statistic type to **Sum**
* Click **Create Widget**

## Important - Save your Cloudwatch Dashboard! ##

# Checkpoint

At this time, your application should be running in both regions. Hit the secondary **SecondaryLoadBalancerDNS** that you copied earlier. You should see the exact same site you had before.

Proceed to [Lab 4](../lab-4-globalacc)!


<!--
# disregard

In this section, you will begin preparations for moving your application to multiple regions. It's very common to forget a number of steps along the way as many people will mainly think of infrastructure and the application itself to move over, but there are a number of assets that also need to be referenced.

These are the things that we will need to replicate and also automate:
* Infrastructure
  * Network
  * Docker Repositories
  * ECS
* Container images
* Application Deployments


- Also need to copy over artifacts for deployment
- ECR cross region replication?
- object replication in S3
- codecommit x-region app
-



### Replicate The app to a second region

    aws cloudformation deploy --stack-name second-region --template-file core.yml --capabilities CAPABILITY_NAMED_IAM --region us-west-2 -->
