# Mythical Mysfits: Multi-Region-Workshop

## Lab 5 - Load test your multi-region application
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

### Invoking the Like service via the CLI
In order to easily run a continuous load test, we need to be able to simulate a user clicking on the heart for a Mysfit to Like them. Thankfully, this is straight forward. When you click Like within the UI of the webapp, it sends a HTTP POST request to the Mysfits Like service. The ID of the Mysfit is contained within the URI of the request and the Like service uses this Mysfits ID in order to know which Mysfit to apply the Like to within the DDB table.

**Important note - AB requires that we specify a "[postfile](https://httpd.apache.org/docs/2.4/programs/ab.html)" as part of our POST request, which would normally contain the HTTP payload. We do not need to send a payload as part of this test, however AB still expects it. Therefore, we need to ceate a blank postfile otherwise AB will error.**
To do this, create an empty postfile using this command:

`touch postfile.txt`

Now we can specify it as part of our **ab** command:

`ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/ <--note the ending forward slash` 

Now lets add in the remaining path to call the Like service, along with one of our Mysfits IDs:

`ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

Calling the above, AB will only send a single POST request once every 2s to our endpoint. Lets preface with the linux command **[watch](https://linux.die.net/man/1/watch)**. The use of Watch is helpful here - as it will execute the AB command repeatedly until we instruct it to stop, keeping things simple for the purposes of testing.

Taking everything into account from the above, lets make sure we understand what the command is doing and provide an example:

* **watch** - repeat the following command
* **ab** - Apache Bench load genetator
* **-p** flag specifies that we are sending a HTTP POST request
* **postfile.txt** - specifies the empty payload file required for AB to send a POST request
* **http:/<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like** - the full URI of what we're POSTing to.

Example -
`watch ab -p postfile.txt http://a174d65be73381239e.awsglobalaccelerator.com/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

### 5.1 Run AB against the stack in the Primary region to test it is working correctly
Navigate to the Global Accelerator Listener and edit the Endpoint groups Traffic Dial to send 100% traffic to Primary region

![image](https://user-images.githubusercontent.com/23423809/68568370-401f4380-0410-11ea-9fb9-4804916f3520.png)

Enter the following command to send some HTTP requests using Apache Bench to our application, via the Cloud9 CLI

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

For example: **watch ab -p postfile.txt http://a174d65be73381239e.awsglobalaccelerator.com/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like**

![image](https://user-images.githubusercontent.com/23423809/68568756-52e64800-0411-11ea-8dcd-429d922b1fea.png)

Apache Bench is now sending HTTP requests to our endpoint and will continue to do so until we stop the watch process. Lets leave this running for a couple of minutes - the aim is to see that our Cloudwatch metrics are populating. *(Note - you can press **Control+C** to stop the test now if you want and resume later)*

If you encounter an error that says:
*ab: Could not open POST data file (postfile.txt): No such file or directory*, then you have not specified an empty postfile. See the Important Note in a previous step.

Next, navigate to the Cloudwatch Dashboard that you created in Lab 2. You should see the different widgets that you have set up within your dashboard begin to have data points in them for the Primary region. You may need to change the refresh intervel to auto-refresh every 10s and the timeframe to **custom (30m)** to see the new metrics come in.

![image](https://user-images.githubusercontent.com/23423809/68569556-3c40f080-0413-11ea-8364-c2b9759b5c90.png)

Once you see the widgets come to life within the Cloudwatch dashboard, this step is complete. You have confirmed that the application in Region A is working correctly *and* that your Cloudwatch dashboard is populating with data correctly. Horray! Now navigate back to Cloud9 and stop the test by pressing **Control+C** in the terminal window.

### 5.2 Run AB against the stack in the Secondary region to test it is working correctly
Next, we will run the same tests as in the previous step, but for the Secondary region.

Navigate to the Global Accelerator Listener and edit the Endpoint groups Traffic Dial to send 100% traffic to the Seconday region

**SCREENSHOT TO BE UPDATED**
![image](https://user-images.githubusercontent.com/23423809/68568370-401f4380-0410-11ea-9fb9-4804916f3520.png)

Enter the following command to send some HTTP requests using Apache Bench to our application, via the Cloud9 CLI

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

![image](https://user-images.githubusercontent.com/23423809/68568756-52e64800-0411-11ea-8dcd-429d922b1fea.png)

Apache Bench is now sending HTTP requests to our endpoint and will continue to do so until we stop the watch process. Lets leave this running for a couple of minutes - the aim is to see that our Cloudwatch metrics are populating. *(Note - you can press **Control+C** to stop the test now if you want and resume later)*

Next, navigate to the Cloudwatch Dashboard that you created in Lab 2. You should see the different widgets that you have set up within your dashboard begin to have data points in them for the Secondary region. At the same time, you'll see traffic drop-off for the Primary region widgets.

Once you see the widgets come to life for the Secondary region within the Cloudwatch dashboard, this step is complete. You have confirmed that the application in this region is working correctly *and* that your Cloudwatch dashboard is populating with data correctly. Double horray! Now navigate back to Cloud9 and stop the test by pressing **Control+C** in the terminal window.

### 5.3 Set the Traffic Dials within our Global Accelerator Endpoint group to split traffic 50% to each region

Navigate back to the Global Accelerator Listener and modify the Endpoint groups to send 50% of traffic to the Primary region and 50% to the Secondary region. By sending half the traffic to one region and half the traffic to the other, we are creating a simple yet effective multi-region setup and using the Global Accelerator as a method of easily directing traffic between the two regions. This can be useful if you need to switch between a Primary and Secondary region for DR purposes, or if you want to test out a modified version of your architecture in a different region with a limited amount of traffic passing through it.

![image](https://user-images.githubusercontent.com/23423809/68570101-b1f98c00-0414-11ea-8d75-01a1a168a693.png)

Start the Apache Bench test again with the same command as previously used (or press UP on the keyboard).

`watch ab -p postfile.txt http://<Insert your Global Accelerator Endpoint>/mysfits/da5303ae-5aba-495c-b5d6-eb5c4a66b941/like`

Next, go back to the Cloudwatch dashboard, wait a few minutes and you should see metrics populate the dashboard widgets across both regions.

### 5.4 Manually failover the Traffic Dial between Regions (optional)

If you want to test out the Traffic Dial feature of the Global Accelerator some more, in order to become more familiar with it, now is a good time. To do this, navigate back to the Global Accelerator Listener page and modify the Traffic Dials and watch how the Cloudwatch dashboard metrics respond. For example, if you set the Primary region to 90% and the Secondary region to 10%, after a few minutes you should notice substantially more traffic being served from the Primary region's metrics in the Cloudwatch dashboard. While in theory this sounds obvious, it is good to see it working in practice.

### 5.5 Artificially "break" the application in Primary region to force failover to Secondary

Before we trigger a failover of the application between regions, it is important to understand how the Global Accelerator knows whether or not the ALB endpoint within each of the regions is healthy or not. As the entry point to each stack in each region in this example is an Application Load Balancer, the Global Accelerator uses the same healthcheck settings as defined in the ALB within the region. In short, if the ALB to our Mythical Mysfits stack within region becomes "unhealthy", the Global Accelerator deems this endpoint to be unavailable and redirects all traffic to other healthy endpoints defined within our Global Accelerator Listener. (You can read more on how this works within the [documentation](https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html#about-endpoint-groups-automatic-health-checks)).

Kick off the AB command to start sending some traffic to the Global Accelerator.

Next, lets force the ALB within our Primary region into an unhealthy state by stopping the Mysfits and Like tasks in our ECS cluster. Once these are stopped, the ALB healthchecks will fail. To do this we need to set the "Desired Tasks" to 0 for each service.

* Within the AWS Management Console, navigate to the ECS Service. Select the Cluster running our services
* Under the Services tab, select the Like-Service, click **Update*
* Set the **Number of tasks** to 0, click **Skip to review** and then click **Update Service**
* Click **View Service** to return to the Service screen

Repeat the above steps for the Mythical-Service.

ECS will update the service and drain any existing connections from the running tasks. This will cause the ALB to fail its healthchecks and therefore fail the Global Accelerator healthchecks for the endpoint in this region.

Your Cloudwatch dashboard should now reflect the traffic pattern expected - within a couple of minutes, you should see that the Primary region is no longer serving requests for the Like service and that the Secondary region is accepting all the traffic.

[INSERT SCREENSHOT OF DASHBOARD]
