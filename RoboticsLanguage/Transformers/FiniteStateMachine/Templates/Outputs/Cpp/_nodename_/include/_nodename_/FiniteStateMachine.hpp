#include <map>
#include <string>
#include <iostream>

class FiniteStateMachine {

private:
  // A machine is a dictionary of states, each having a set of transitions.
  // { state: { transition -> state, ... } }
  // For example:
  // States: 'idle', 'running'
  // Transitions: 'start', 'stop'
  // Representation:
  // { 'idle': { 'start' -> 'running'}, 'running' : { 'stop' -> 'idle'} }
	std::map<std::string, std::map<std::string, std::string> > machine;

  // list of function types: init, exit, inside, global
	std::map<std::string, std::map<std::string, std::function<void()> > > functions;

  // The current state
	std::string current_state;

  // last transition
	std::string last_transition;

  // the name of the state machine
  std::string name;

  // publisher for HTML GUI
  std::function<void(std::string)> state_feedback_publisher;

  // check if state exists
  bool state_exists_(std::string state_)
  {
    return (machine.find(state_) != machine.end());
  }

  bool function_exists_(std::string type_, std::string state_)
  {
    auto function_type = functions.find(type_);
    if (function_type == functions.end())
    {
      return false;
    }
    else
    {
      return ((function_type->second).find(state_) != (function_type->second).end());
    }
  }



public:
	FiniteStateMachine(std::string name_ = "")
		{
      // always start uninitialised
      current_state = "";
      name = name_;

      // create structures for functions
      std::map<std::string, std::function<void()> > init_type, exit_type, inside_type, global_type;

      // add to main structures
      functions.insert(std::pair<std::string, std::map<std::string, std::function<void()> > >("init", init_type));
      functions.insert(std::pair<std::string, std::map<std::string, std::function<void()> > >("exit", exit_type));
      functions.insert(std::pair<std::string, std::map<std::string, std::function<void()> > >("inside", inside_type));
      functions.insert(std::pair<std::string, std::map<std::string, std::function<void()> > >("global", global_type));

		};

	~FiniteStateMachine(){};

  void addStateFeedbackPublisher(std::function<void(std::string)> state_feedback_publisher_)
  {
    state_feedback_publisher = state_feedback_publisher_;
  }

  void publishState()
  {
    if (state_feedback_publisher)
    {
      state_feedback_publisher(current_state);
    }
  }


  // void addStateFeedbackPublisher(ros::Publisher *state_feedback_publisher_)
  // {
  //   state_feedback_publisher = state_feedback_publisher_;
  // }

  // void publishState()
  // {
  //   if (state_feedback_publisher != 0)
  //   {
  //     state_message.data = current_state;
  //     state_feedback_publisher->publish(state_message);
  //   }
  // }

	bool addState(std::string name)
  {
    if (!state_exists_(name))
    {
      try
      {
        // explicitely create transition structure
    		std::map<std::string, std::string> transition;

        // add new state to machine
    		machine.insert(std::pair<std::string, std::map<std::string, std::string> >(name, transition));

        return true;
      }
      catch (std::exception & e)
      {
        return false;
  		}
    }
    else
    {
      return false;
    }
	}

	bool addTransition(std::string arc, std::string begin, std::string end) {
		try
    {
      // create begin state if needed
      if (!state_exists_(begin))
      {
        addState(begin);
      }

      // create end state if needed
      if (!state_exists_(end))
      {
        addState(end);
      }

      // add transition
      machine[begin].insert(std::pair<std::string, std::string>(arc, end));

      return true;
		}
    catch (std::exception & e)
    {
      return false;
		}
	}

  bool setInitialState(std::string state_)
  {
    if (current_state == "")
    {
      current_state = state_;

      return true;
    }
    else
    {
      return false;
    }
  }

  bool fire(std::string transition)
  {
    // find the transition
    auto current_transition = machine[current_state].find(transition);

    // if defined for the current state
    if (current_transition != machine[current_state].end())
    {
      // first run the exit function
      runExitFunction();

      // change state
      current_state = current_transition->second;

      publishState();

      // remember last transition
      last_transition = transition;

      // finally run the init function
      runInitFunction();

      return true;
    }

    return false;
  }


  bool addFunction(std::function<void()> function_, std::string type_, std::string state_)
  {
    try
    {
      // insert function
      functions[type_].insert(std::pair<std::string, std::function<void()> >(state_, function_));

      return true;
    }
    catch (std::exception & e)
    {
      return false;
    }
  }


  bool addInitFunction(std::function<void()> function_)
  {
    return addFunction(function_, "global", "init");
  }

  bool addInitFunction(std::function<void()> function_, std::string state_)
  {
    return addFunction(function_, "init", state_);
  }

  bool addExitFunction(std::function<void()> function_)
  {
    return addFunction(function_, "global", "exit");
  }

  bool addExitFunction(std::function<void()> function_, std::string state_)
  {
    return addFunction(function_, "exit", state_);
  }

  bool addInsideFunction(std::function<void()> function_)
  {
    return addFunction(function_, "global", "inside");
  }

  bool addInsideFunction(std::function<void()> function_, std::string state_)
  {
    return addFunction(function_, "inside", state_);
  }



	std::string state()
	{
		return current_state;
	}

  std::string lastTransition()
	{
		return last_transition;
	}


private:

  void runInitFunction()
  {
    if (function_exists_("global","init"))
    {
      functions["global"]["init"]();
    }

    if (function_exists_("init",current_state))
    {
      functions["init"][current_state]();
    }
  }

  void runExitFunction()
  {
    if (function_exists_("global","exit"))
    {
      functions["global"]["exit"]();
    }

    if (function_exists_("exit",current_state))
    {
      functions["exit"][current_state]();
    }
  }

public:

  void runInsideFunction()
  {
    if (function_exists_("global","inside"))
    {
      functions["global"]["inside"]();
    }

    if (function_exists_("inside",current_state))
    {
      functions["inside"][current_state]();
    }
  }

	void show() {
    std::cout << "\n\n\nFinite State Machine: " << name << std::endl;

		for (auto state_iterator = machine.begin(); state_iterator != machine.end(); state_iterator++)
    {
			std::cout << "State: " << state_iterator->first << std::endl;

      std::cout << "Transitions:" << std::endl;

      for (auto transition_iterator = state_iterator->second.begin();
           transition_iterator != state_iterator->second.end(); transition_iterator++)
      {
				std::cout << "   " << transition_iterator->first << " : " << state_iterator->first
            << " -> " << transition_iterator->second << std::endl;
			}
			std::cout << std::endl;
		}
	}
};
