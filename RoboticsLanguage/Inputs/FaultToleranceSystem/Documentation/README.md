# Fault Tolerance system Documentation

![](images/architecture.png)


The Fault Tolerance system consists of a collection of nodes that deal with faults and failures:

 - **Fault** is defined as an abnormal condition or defect at the component, equipment, or sub-system level which may lead to a failure.

 - **Failure**  is the state or condition from where it is not possible for a system to continue to function. Failures lead to system shutdown.

This implementation includes the following classes of nodes:

- [**Fault Detection Topics**](../../FaultDetectionTopics/Documentation/README.md) - Monitors content of topics and issues faults.

- [**Fault Detection Heartbeat**](../../FaultDetectionHeartbeat/Documentation/README.md) - Monitors if nodes are operating by measuring a heartbeat topic.

- [**Fault Detection Processes**](../../FaultDetectionProcesses/Documentation/README.md) - Monitors if nodes are operating by using operative system level tools, such as `ps`.

- [**Fault Handler**](../../FaultHandler/Documentation/README.md) - Acts on faults by generating recovery actions or by escalating into failures.

- [**Failure Handler**](../../FailureHandler/Documentation/README.md) - Acts on failures by generating shutdown actions.