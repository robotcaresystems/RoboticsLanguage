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
  // { 'idle': { 'start' -> 'running'}, 'running' : { 'stop' -> 'start'} }
	std::map<std::string, std::map<std::string, std::string> > machine;

  // list of functions that are executed on entry, exit, or inside the state
	std::map<std::string, std::function<void()> > init_function, exit_function, inside_function;

  // The current state
	std::string current_state;

  // the name of the state machine
  std::string name;

  // check if state exists
  bool state_exists_(std::string state)
  {
    return (machine.find(state) != machine.end());
  }

public:
	FiniteStateMachine(std::string name_ = "")
		{
      // always start uninitialised
      current_state = "";
      name = name_;
		};

	~FiniteStateMachine(){};

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

  bool setInitialState(std::string state)
  {
    if (current_state == "")
    {
      current_state = state;

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
      auto current_exit = exit_function.find(current_state);
      if (current_exit != exit_function.end()) {
				(current_exit->second)();
			}

      // change state
      current_state = current_transition->second;

      // finally run the init function
      auto current_init = init_function.find(current_state);
      if (current_init != init_function.end()) {
				(current_init->second)();
			}

      return true;
    }

    return false;
  }



	bool addInitFunction(std::string state, void (*function)())
  {
    try
		{
			init_function.insert(std::pair<std::string, std::function<void()> >(state,(*function)));

      return true;
    }
    catch (std::exception & e)
    {
      return false;
    }
	}


  bool addExitFunction(std::string state, void (*function)())
  {
    try
		{
			exit_function.insert(std::pair<std::string, std::function<void()> >(state,(*function)));

      return true;
    }
    catch (std::exception & e)
    {
      return false;
    }
	}

  bool addInsideFunction(std::string state, void (*function)())
  {
    try
		{
			inside_function.insert(std::pair<std::string, std::function<void()> >(state,(*function)));

      return true;
    }
    catch (std::exception & e)
    {
      return false;
    }
	}


	std::string currentState()
	{
		return current_state;
	}


  void runInsideFunction()
  {
    auto current_inside = inside_function.find(current_state);
    if (current_inside != inside_function.end()) {
      (current_inside->second)();
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
