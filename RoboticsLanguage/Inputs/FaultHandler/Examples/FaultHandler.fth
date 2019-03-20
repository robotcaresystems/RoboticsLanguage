nodename: Fault handler

parameters:
  float_parameter: 5.6
  integer_parameter: 2
  string_parameter: hello

topics:
  fault: /fault rrc_msgs/Fault
  failure: /failure rrc_msgs/Failure
  action: /action rrc_msgs/Action
  terminator: /terminator/kill std_msgs/String
  x: /test/integer std_msgs/Int8
  y: /test/float std_msgs/Float32
  z: /test/string std_msgs/String
  w: /test/struct geometry_msgs/Pose
  q: /test/array std_msgs/Float32MultiArray

faults:
    - fault: hb_supervisor
      action:
        code: >
          terminator = "supervisor"
      retry: 3
      timeout: 5
      on_fail:
        failure: fa_supervisor

    - fault: hb_navigator
      retry: 3
      timeout: 5
      on_fail:
        failure: fa_navigator
      action:
        code: >
          if(x>0,
            failure = "FA002",
            if(state == "navigation",
              block(
                Shell<{ restart_navigation }>,
                return(true)
              ),
              return(false)
            )
