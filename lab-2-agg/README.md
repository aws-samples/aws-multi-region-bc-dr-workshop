# Mythical Mysfits: Multi-Region-Workshop

## Lab 2 - Gather AWS Metrics

In this lab, you will start the process of aggregating metrics to understand the health of your application so you can make informed decisions about when to fail over to a different region. We will use an Amazon Cloudwatch Dashboard, amongst other stuff.

Our Cloudwatch dashboard should include metrics from the key components of our system and application. In this case, the metrics we should display on a dashboard are the following:

* Fargate task capacity (CPU / Mem)
* ALB requests per minute
* Number of "Likes" to our Fargate service
* X-Ray exposed metric to dashboard?

Here's a reference image showing the metrics that we'll be putting onto a dashboard -
![image](https://user-images.githubusercontent.com/23423809/69004118-aac5f880-08c2-11ea-9ace-ffd63a3aee25.png)

Here's what you'll be doing:

* Create Amazon Cloudwatch Dashboard
* Add metrics to the dashboard
* Save the dashboard



### 2.1 Create Amazon Cloudwatch Dashboard

1\. Open Amazon Cloudwatch

From the AWS Management Console, select Services and then type **Cloudwatch** into the search bar. You can also find it under the Management and Governance section of the services listing. This will bring up the Amazon Cloudwatch service overview page.

2\. Create a new Cloudwatch dashboard and add a widget

From the menu on the left hand side, select **Dashboards** and then create dashboard. This will prompt you for a name - call it ReInvent App Dashboard and then click Create Dashboard.
* Note - Cloudwatch does not allow spaces in a dashboard name, so will fill in spaces with a hyphen!
![image](https://user-images.githubusercontent.com/23423809/68278028-5babd800-0025-11ea-9a96-b4fc213acdd8.png)

You will be prompted to select a widget to add to your dashboard. Start off by selecting a line widget and click Configure. We will use this widget to map out our number of requests per minute passing through our Application Load Balancer. This will be useful to show that there is actual traffic passing through the LB to the backend application.

![image](https://user-images.githubusercontent.com/23423809/68278128-931a8480-0025-11ea-8d88-721856aeb3dc.png)

We will add our first metric - ALB Requests Per Minute - to the Cloudwatch dashboard.
This is the *RequestCount* metric under the *ApplicationELB* Namespace. Select it by selecting **ApplicationELB -> Per AppELB Metrics** and then selecting the tickbox next to **RequestCount**.

![image](https://user-images.githubusercontent.com/23423809/68278987-594a7d80-0027-11ea-8a43-acd4f8c073d2.png)

Next, select the tab marked *Graphed Metrics*, change the Period to 1 Minute and change the Statistic to *Sum*. (Tip - we know that Sum is the most useful statistic to use, as the [Cloudwatch documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html#load-balancer-metrics-alb) gives us a recommendation like this for each metric).

Give your widget a name by pressing the pencil next to *Untitled Graph*, inputting a name (e.g. ALB Requests Per Minute), click on the little tick-box and click **Create widget**.

![image](https://user-images.githubusercontent.com/23423809/68279497-65830a80-0028-11ea-8c7a-f76970713829.png)

You have now created your first dashboard and added your first widget! Make sure to **Save your dashboard!!** by clicking the button *Save Dashboard*.

3\. Repeat the steps above to add additional widgets to your dashboard using the details below to determine which metric to use. These are just an example, of course you can use any other metrics that are meaningful to you.

#### Mythical Service Metrics - CPU and Memory utilization of our Mythical Fargate Service
- Widget type - number
- Metric location - ECS -> ClusterName, ServiceName -> CPUUtilization and MemoryUtilization (make sure ServiceName is for Mythical Service)
- Widget Title - Like Service Metrics

#### Like Service Metrics - CPU and Memory utilization of our Like Fargate Service
- Widget type - number
- Metric location - ECS -> ClusterName, ServiceName -> CPUUtilization and MemoryUtilization (make sure ServiceName is for Like Service)
- Widget Title - Mythical Service Metrics

#### ALB HTTP Responses - Graph showing the different HTTP responses from the backend servers
- Widget type - Stacked Graph
- Metric location -> ApplicationELB -> Per AppELB Metrics -> HTTPCode_Target_2XX_Count, HTTPCode_Target_4XX_Count, HTTPCode_Target_5XX_Count (ensure app/alb-<your_stack_name> shows as the LoadBalancer)
- Statistic - Sum
- Period - 1 Minute

#### KPI From X-Ray here
(this is still TBD obtaining the metric data from x-ray service)

#### Number of HTTP POSTS to Like Service
(this is still TBD whether we want to put this in here)

### Remember to save your dashboard!!

### 2.2 HEADER

# Checkpoint

Proceed to [Lab 3](../lab-3-mr-prep)!
