/*
 *  rol_timer.hpp
 *
 *  Created on: November 1, 2018
 *      Author: Dimitrios Chronopoulos
 *   Copyright: 2014-2018 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
 *
 */

#include <iostream>
#include <thread>
#include <chrono>
#include "rol_sleep.hpp"

#ifndef ROL_UTILS_ROL_TIMER_HPP
#define ROL_UTILS_ROL_TIMER_HPP

namespace rol_timer
{
  /**
  * @brief      Class that handles timer-events, i.e. triggers a function-call after a specific amount of time.
  * @details    The TimerEvent class will call a function after a timeout. The function to be executed can have
  *             an arbitrary number/type of arguments but no return value. The timer can be started and stopped at any
  *             time. A different function, timeout can be used every time the timer starts. If the repeat flag is set
  *             then the timer-event becomes a periodic event.
  *
  *             This code is a (moderately) modified version of the answer found here:
  *             https://stackoverflow.com/questions/21521282/basic-timer-with-stdthread-and-stdchrono
  */
  class TimerEvent
  {

    public:
      /**
       * @brief   Constructor 1: repeat is false by default
       */
      TimerEvent()
      :
        TimerEvent(false)
      {};

      /**
       * @brief   Constructor 2
       *
       * @param   repeat  Whether to repeat the event_cb
       */
      TimerEvent(bool repeat)
      :
        repeat_(repeat)
      {};

      /**
       * @brief   Destructor: ensures the thread exits and joins cleanly
       *
       * @param   repeat  Whether to repeat the event_cb
       */
      ~TimerEvent()
      {
        stopTimer();
      };


      /**
       * @brief   Stops the previous timer and wraps the new timer event with a thread
       *
       * @param   timeout   The sleep duration [chrono literal]
       * @param   event_cb  The callback to be executed after the timeout
       * @param   args      The arguments to be given to the callback
       */
      template <typename DurationT, class... Args>
      void startTimer(
        const std::chrono::duration< int64_t, DurationT >& timeout,
        std::function< void() > event_cb,
        Args&&... args
      )
      {
        // Stop the previous thread
        if (thread_.joinable())
        {
          stopTimer();
        }

        // Start a new timer
        running_ = true;
        thread_ = std::thread(std::bind(&TimerEvent::timerThread< DurationT, Args... >, this, timeout, event_cb, args...));
        return;
      }

      /**
       * @brief   The timer thread that handles the sleep timeout and executing the callback
       *
       * @param   timeout   The sleep duration [chrono literal]
       * @param   event_cb  The callback to be executed after the timeout
       * @param   args      The arguments to be given to the callback
       */
      template <typename DurationT, class... Args>
      void timerThread(
        const std::chrono::duration< int64_t, DurationT >& timeout,
        std::function< void() > event_cb,
        Args&&... args
      )
      {
        while (running_)
        {
          // Sleep for the timeout
          sleeper_.sleep(timeout);
          // We only execute the function if we woke from sleep normally
          if (running_)
          {
            // Execute the function
            event_cb(args...);

            // Lower the flag if we are not repeating
            if (!repeat_){
              running_ = false;
            }
          }
        }
        return;
      }
      /**
       * @brief   Stops the current timer and ensures the timer thread joins
       */
      void stopTimer()
      {
        // Only stop if there is a thread
        if (!thread_.joinable())
        {
          return;
        }

        // Lower the flag and wake the sleeper so the thread can exit
        running_ = false;
        sleeper_.wake();
        // Wait for the thread to join
        thread_.join();
        return;
      }

    private:

      rol_sleep::Sleeper sleeper_; /**< An interruptable sleeper */
      std::thread thread_;         /**< The thread that handles sleeping and executing the event callback */

      bool running_; /**< Whether the timer loop should be running */
      bool repeat_;  /**< Whether to repeat the thread loop */
  };

} // namespace rol_sleep

#endif // ROL_UTILS_ROL_TIMER_HPP
