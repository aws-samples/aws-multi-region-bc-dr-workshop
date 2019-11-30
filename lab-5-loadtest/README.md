# Mythical Mysfits: Building Multi-Region Applications that Align with BC/DR Objectives

## Workshop progress
✅ [Lab 0: Workshop Initialization](../lab-0-init)

✅ [Lab 1: Instrument Observability - Distributed Tracing with AWS X-Ray](../lab-1-xray)

✅ [Lab 2: Operationalize Observability - Aggregate Metrics](../lab-2-agg)

✅ [Lab 3: Preparing for Multi-Region Deployments](../lab-3-mr-prep)

✅ [Lab 4: Implement Traffic Management - Global Accelerator](../lab-4-globalacc)

**Lab 5: Load Test and Failover your multi-region application**

## Lab 5 - Load Test and Failover your multi-region application
Now that we have the Global Accelerator set up and targetting our two different Load Balancers residing in each region, lets send some test traffic to it. The aim of this lab is to learn how to use the Global Accelerator to manipulate traffic flows and then use this method to direct traffic for our **Like** service between regions. This will be useful when there is a need to failover between our regions to meet our Service Level Objectives.
One of the benefits of using the Global Accelerator in this scenario is that we do not need to wait for DNS TTL's (Time To Live) to expire, nor rely on them. Instead the Global Accelerator provides a single DNS endpoint with two A-records behind it. We only need to send traffic to the single DNS endpoint for the traffic manipulation to be effective.
In addition, we will learn how to use the Global Accelerator Health Checks to automatically direct traffic away from a region where the application is showing an unhealthy state over to another region where the app is healthy.

To do this, we will use [Apache Bench](https://httpd.apache.org/docs/2.4/programs/ab.html) (AB) to generate some HTTP requests to our Global Accelerator Endpoint from our Cloud9 environment. Apache Bench is a simple command line based tool that can be used to benchmark a webserver and is already installed within our Cloud9 environment. AB will send a consistent number of HTTP **POST** requests to our Like service . *Note - The Like service only accepts a HTTP POST request. A HTTP GET will return an error*)

At a high-level, during this lab we will -
* Run AB against the stack in the Primary region to test it is working correctly
* Run AB against the stack in the Seconday region to test it is working correctly
* Set the Traffic Dials within our Global Accelerator Endpoint group to split traffic 50% to each region
* Manually failover the Traffic Dial between Regions (optional)
* Artificially "break" the application stack in one region to force failover by the Global Accelerator

### Quick note about invoking the Like service via the CLI

In order to easily run a continuous load test, we need to be able to simulate a user clicking on the heart for a Mysfit to Like them. Thankfully, this is straight forward. When you click Like within the UI of the webapp [example here](![image](https://user-images.githubusercontent.com/23423809/69885348-91915480-1291-11ea-8b21-dd53350d2781.png)
), it sends a HTTP POST request to the Mysfits Like service. The ID of the Mysfit is the GUID contained within the URI of the request and the Like service uses this Mysfits ID in order to know which Mysfit to apply the Like to within the DDB table. You will use the Mysfit ID in the lab guide below during our testing.



### Instructions

First, lets do some quick quality control on our environments. You will send some test traffic to each region through the Global Accelerator. This will test a number of things:
1. The Global Accelerator is configured correctly and is directing traffic to the correct region.
2. The stack is functionally working in each region and able to serve back valid responses.
3. The Cloudwatch dashboard is showing us good data as it updates to reflect the traffic serving each region.

### [1] Create the pre-requisites required for the Apache Bench command to work correctly

Instructions for creating the postfile are located here.

AB requires that we specify a "[postfile](https://httpd.apache.org/docs/2.4/programs/ab.html)" as part of our POST request, which would normally contain the HTTP payload. We do not need to send a payload as part of this test, however AB still expects it. Therefore, we need to ceate a blank postfile otherwise AB will error.

To do this, navigate to our working directory and create an empty **postfile**:

```
cd ~/environment/aws-multi-region-bc-dr-workshop/
touch postfile.txt
```

![image](https://user-images.githubusercontent.com/23423809/69886140-69a3f000-1295-11ea-8d2f-4cc55d79f1d7.png)


### 5.1 Run AB against the stack in the Primary region to test it is working correctly

1. Set the Endpoint Group Traffic Dial within the Global Accelerator to send 100% traffic to Primary region
2. Use Apache Bench to send some traffic to the Global Accelerator (and therefore the Primary region)

```
watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like
```

<details>
  <summary>Learn more: what is this command actually doing?</summary>

AB will only send a single POST request once every 2s to our endpoint so we will preface it with the linux command **[watch](https://linux.die.net/man/1/watch)**. The use of Watch is helpful here - as it will execute the AB command repeatedly until we instruct it to stop, keeping things simple for the purposes of testing.

Taking this into account, lets make sure we understand what the full command is doing:

Example -<br>
```
watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like
```

* **watch** - repeat the following command
* **ab** - Apache Bench load genetator
* **-p** flag specifies that we are sending a HTTP POST request
* **postfile.txt** - specifies the empty payload file required for AB to send a POST request
* **http:<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like** - the full URI of what we're POSTing to.

Example -
`watch ab -p postfile.txt http://a174d65be73381239e.awsglobalaccelerator.com/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

  </details>

3. Confirm the Cloudwatch dashboard is updating accordingly

<details>
  <summary>Hint: step by step instructions</summary>

1. Navigate to the Global Accelerator Listener and edit the Endpoint groups Traffic Dial to send 100% traffic to Primary region

![image](https://user-images.githubusercontent.com/23423809/69886941-61e64a80-1299-11ea-9d65-532218b2d2b3.png)

2. Using CLoud9, enter the following command to send some HTTP requests using Apache Bench to our application

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

For example: watch ab -p postfile.txt http://**a174d65be73381239e.awsglobalaccelerator.com**/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like

![image](https://user-images.githubusercontent.com/23423809/69886638-ce604a00-1297-11ea-996e-bb1975026ca0.png)

Press enter:

![image](https://user-images.githubusercontent.com/23423809/69886679-ff407f00-1297-11ea-892a-890a26c7abd1.png)

Apache Bench is now sending HTTP POST requests to our endpoint and will continue to do so until we stop the watch process. Lets leave this running for a couple of minutes - the aim is to see that our Cloudwatch metrics are populating. *(Note - you can press **Control+C** to stop the test now if you want and resume later)*

If you encounter an error that says:
*ab: Could not open POST data file (postfile.txt): No such file or directory*, then you have not specified an empty postfile. See the Important Note in a previous step.

3. Navigate to the Cloudwatch Dashboard that you created in Lab 2. You should see the different widgets that you have set up within your dashboard begin to have data points in them for the Primary region. You may need to change the refresh intervel to auto-refresh every 10s and the timeframe to **custom (30m)** to see the new metrics come in.

![image](https://user-images.githubusercontent.com/23423809/68569556-3c40f080-0413-11ea-8364-c2b9759b5c90.png)

</details>

Once you see the widgets come to life within the Cloudwatch dashboard, this step is complete. You have confirmed that the application in Region A is working correctly *and* that your Cloudwatch dashboard is populating with data correctly. Horray! Now navigate back to Cloud9 and stop the test by pressing **Control+C** in the terminal window.

### 5.2 Run AB against the stack in the Secondary region to test it is working correctly
Next, we will run the same tests as in the previous step, but for the Secondary region.

1. Set the Endpoint Group Traffic Dial within the Global Accelerator to send 100% traffic to Secondary region
2. Use Apache Bench to send some traffic to the Global Accelerator (and therefore the Secondary region)

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

3. Confirm the Cloudwatch dashboard is updating accordingly

<details>
  <summary>Hint: step by step instructions</summary>

1. Navigate to the Global Accelerator Listener and edit the Endpoint groups Traffic Dial to send 100% traffic to the Seconday region

![image](https://user-images.githubusercontent.com/23423809/69886988-9528d980-1299-11ea-8dea-9983d0b685db.png)

2. Enter the following command to send some HTTP requests using Apache Bench to our application, via the Cloud9 CLI

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

Apache Bench is now sending HTTP requests to our Global Accelerator endpoint and will continue to do so until we stop the watch process. Lets leave this running for a couple of minutes - the aim is to see that our Cloudwatch metrics are populating. *(Note - you can press **Control+C** to stop the test now if you want and resume later)*

3. Navigate to the Cloudwatch Dashboard that you created in Lab 2. You should see the different widgets that you have set up within your dashboard begin to have data points in them for the Secondary region. At the same time, you'll see traffic drop-off for the Primary region widgets.

</details>

Once you see the widgets come to life for the Secondary region within the Cloudwatch dashboard, this step is complete. You have confirmed that the application in this region is working correctly *and* that your Cloudwatch dashboard is populating with data correctly. Double horray! Now navigate back to Cloud9 and stop the test by pressing **Control+C** in the terminal window.

### 5.3 Set the Traffic Dials within our Global Accelerator Endpoint group to split traffic 50% to each region

Once you are happy that the Cloudwatch dashboard is showing the correct data, you will split traffic equally between the two regions.  By sending half the traffic to one region and half the traffic to the other, we are creating a simple yet effective multi-region setup and using the Global Accelerator as a method of easily directing traffic between the two regions. This can be useful if you need to switch between a Primary and Secondary region for DR purposes, or if you want to test out a modified version of your architecture in a different region with a limited amount of traffic passing through it.

1. Navigate back to the Global Accelerator Listener and modify the Endpoint groups to send 50% of traffic to the Primary region and 50% to the Secondary region.

![image](https://user-images.githubusercontent.com/23423809/69887101-1bddb680-129a-11ea-9efa-b3b09aa84024.png)

2. Start the Apache Bench test again with the same command as previously used (or press UP on the keyboard).

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

3. Go back to the Cloudwatch dashboard, wait a few minutes and you should see metrics populate the dashboard widgets across both regions.

![image](https://user-images.githubusercontent.com/23423809/69887455-d7ebb100-129b-11ea-8f6c-1f091dacfde5.png)

**Note - your dashboard will not look exactly like this, screenshot above is for reference only**

### 5.4 Manually failover the Traffic Dial between Regions (optional)

If you want to test out the Traffic Dial feature of the Global Accelerator some more, in order to become more familiar with it, now is a good time. To do this, navigate back to the Global Accelerator Listener page and modify the Traffic Dials and watch how the Cloudwatch dashboard metrics respond. For example, if you set the Primary region to 90% and the Secondary region to 10%, after a few minutes you should notice substantially more traffic being served from the Primary region's metrics in the Cloudwatch dashboard. While in theory this sounds obvious, it is good to see it working in practice.

### 5.5 Artificially "break" the application in Primary region to force failover to Secondary

Before we trigger a failover of the application between regions, it is important to understand how the Global Accelerator knows whether or not the ALB endpoint within each of the regions is healthy or not. As the entry point to each stack in each region in this example is an Application Load Balancer, the Global Accelerator uses the same healthcheck settings as defined in the ALB within the region. In short, if the ALB to our Mythical Mysfits stack within region becomes "unhealthy", the Global Accelerator deems this endpoint to be unavailable and redirects all traffic to other healthy endpoints defined within our Global Accelerator Listener. (You can read more on how this works within the [documentation](https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html#about-endpoint-groups-automatic-health-checks)).

**PLEASE READ: You have some options at this point:**

1. Break the application by stopping the ECS tasks in one region.
2. Modify the Access Control List (ACL) in a region to force the Application Load Balancer healthcheck to fail.

<details>
  <summary>Option 1: Break the application by stopping the ECS tasks in one region.</summary>

Kick off the AB command to start sending some traffic to the Global Accelerator.

Next, lets force the ALB within our Primary region into an unhealthy state by stopping the Mysfits and Like tasks in our ECS cluster. Once these are stopped, the ALB healthchecks will fail. To do this we need to set the "Desired Tasks" to 0 for each service.

1. Within the AWS Management Console, navigate to the ECS Service. Select the Cluster running our services
2. Under the Services tab, select the Like-Service, click **Update*
3. Set the **Number of tasks** to 0, click **Skip to review** and then click **Update Service**
4. Click **View Service** to return to the Service screen

Repeat the above steps for the Core-Service.

ECS will update the service and drain any existing connections from the running tasks. This will cause the ALB to fail its healthchecks and therefore fail the Global Accelerator healthchecks for the endpoint in this region.

Your Cloudwatch dashboard should now reflect the traffic pattern expected - within a couple of minutes, you should see that the Primary region is no longer serving requests for the Like service and that the Secondary region is accepting all the traffic.

</details>

<details>
  <summary>Option 2: Modify the Access Control List (ACL) in a region to force the Application Load Balancer healthcheck to fail</summary>

We will simulate a configuration change in a region that results in the ALB being unable to contact the container instances for the application. This configuration change will force the ALB healthchecks to fail and therefore fail the Global Accelerator healthchecks for the endpoint in this region.  

1. Within the AWS Management Console, navigate to the ECS Service. Select the Cluster running our services
2. Under the Services tab, Select the **Core** service.
3. Click the security group un the Details tab which will bring you to the Security Groups section of EC2:

![image](https://user-images.githubusercontent.com/23423809/69887790-90febb00-129d-11ea-91e5-9e2ce3f6f25b.png)

4. Modify the security group click clicking the **Inbound Rules** tab at the bottom and click **Edit rules**.
5. This rule currently allows all TCP traffic from source 10.0.0.0/16 (our VPC CIDR). Edit the rule to reflect 10.0.0.0/32 - this will break the Load Balancer healthchecks as it will not allow the ALB to communicate with this instance.

![image](https://user-images.githubusercontent.com/23423809/69887974-5f3a2400-129e-11ea-8507-dabde34790fd.png)

6. Save the rule.
7. Wait about 30 seconds then, navigate to the Global Accelerator and select your Global Accelerator. You will see the console is informing you that there is a healthy endpoint *(this is correct, we did this in step 5 above)*.

![image](https://user-images.githubusercontent.com/23423809/69888054-c0fa8e00-129e-11ea-9ec2-a94e7f570289.png)

At this time, the Global Accelerator will have redirected all incoming traffic to the remaining healthy endpoints. If you look at the CLoudwatch dashboard, you should see the drop in traffic to the region that you "broke" the application in. This is expected behaviour.

8. Revert the change you made to the security group in step 5 above to bring the application back online and the healthcheck into a healthy state by modifying the source CIDR block to reflect **10.0.0.0/16**.


  </details>
