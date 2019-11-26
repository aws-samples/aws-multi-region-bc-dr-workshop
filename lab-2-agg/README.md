# Mythical Mysfits: Multi-Region-Workshop

## Lab 2 - Gather AWS Metrics

In this lab, you will start the process of aggregating metrics to understand the health of your application so you can make informed decisions about when to fail over to a different region. We will use an Amazon Cloudwatch Dashboard for this.

Our Cloudwatch dashboard should include metrics from the key components of our system and application. In this case, the metrics we should display on a dashboard are the following:

* Fargate task capacity (CPU / Mem)
* ALB requests per minute
* ALB HTTP 200, 400 and 500 responses
* Application faults and errors reported by AWS X-Ray

Here's a reference image showing what your CLoudwatch dashboard may look like when complete -
![image](https://user-images.githubusercontent.com/23423809/69607429-14888580-0fda-11ea-9ec1-bd6ffa16b2b0.png)

Luckily, the previous engineer already started the task of creating the dashboard for you, adding some basic metrics regarding Load Balancer health and the Core and Like service metrics from the ECS Tasks. There are still some additional metrics to add, however. The dashboard can be located by navigating to the Cloudwatch service and selecting <stackname>-Dashboard.

Here's what you'll be doing:

* Open up the pre-configured Cloudwatch dashboard
* Add metrics to the dashboard X-Ray Errors
* Save the dashboard


### 2.1 Open up the pre-configured Cloudwatch dashboard

1. Navigate to the Amazon [Cloudwatch service](https://console.aws.amazon.com/cloudwatch/) from the Management Console
2. Select **Dashboards** from the menu on the left
3. Select the Cloudwatch dashboard that contains the name **Dashboard**

### 2.2 Add metrics to the dashboard for X-Ray Errors and Faults

In the previous Lab, you instrumented the Like service with AWS X-Ray which provides greater visibility into individual requests passing through the Like service. You also created a Trace Group that will filter out the faults and errors that X-Ray has captured from the application. Create a widget on the Cloudwatch dashboard to show the number of errors and faults that X-Ray has observed from the trace information. X-Ray pushes these metrics to Cloudwatch so that we can display them on the dashboard. Use the step by step instructions below if required.

Reminder: [What is an AWS X-Ray trace?](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html#xray-concepts-traces)

<details>
<summary>Step by step instructions:</summary>
  
1. Click on the **Add Widget** button in the Cloudwatch dashboard
  ![image](https://user-images.githubusercontent.com/23423809/69609253-e9a03080-0fdd-11ea-9090-40568a536874.png)

2. Select **Stacked area** and press **configure**

3. Select **X-Ray** followed by **Group Metrics** and select the Group created in the X-Ray lab previously
![image](https://user-images.githubusercontent.com/23423809/69609559-a8f4e700-0fde-11ea-89aa-9375ce0db044.png)

4. Select the tab maked **Graphed metrics** and change the Statistic to **Sum**. Press **Create widget**
![image](https://user-images.githubusercontent.com/23423809/69609745-1acd3080-0fdf-11ea-9958-70416f6408f0.png)

5. Move the widget to whereever you want to on the dashboard
6. Save the dashboard by pressing **Save dashboard**

</details>

# Checkpoint

Proceed to [Lab 3](../lab-3-mr-prep)!
