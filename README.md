# Social Network Analysis using Big Data Technologies 
## Course : CS 554 (Adam)
### Problem Statement
We will utilize several Big Data approaches to implement a system that would suggest the user with the most similar members who are within n hops from him. We mine for the user's personality traits using his tweets/retweets/likes data. Once we get personality information, we check for traits for the members who are under n hops from the user. Performance in terms of execution time is compared for recommendation of friends with and without Hadoop ecosystem tools.

### Data Source 
`Twitter API`

### Requirements
`khafka`
`pyspark`
`ElasticSearch`
`Kibana`

### Setup
All the implementation and development are done in `Windows`platform </br>

##### `khafka`
  Go to config folder in `Apache Kafka` and edit `server.properties`
 
  #### Running Apache Kafka
  Open `command prompt` and go to your Apache Kafka directory and run following command.
  `.\bin\windows\kafka-server-start.bat .\config\server.properties`
  #### Creating Topic
  Open `command prompt` in Apache Kafka installation directory.
  Run the following command in `\bin\windows directory`.
  `kafka-topics.bat — create — zookeeper localhost:2181 — replication-factor 1 — partitions 1 — topic sql-insert`
  #### Creating Consumer & Producer
  Run the following command in `cmd` to start a producer.
  `kafka-console-producer.bat — broker-list localhost:9092 — topic sql-insert`

##### `pyspark`
 Open `Anacode Terminal` and run the following command 
 `pip install spark` 
 
##### `ElasticSearch`
  Follow the instructions in the link mentioned below :-
  https://www.elastic.co/guide/en/elasticsearch/reference/current/windows.html

##### `Kibana`
  Follow the instructions in the link mentioned below :-
  https://www.elastic.co/guide/en/kibana/current/windows.html
  
  
