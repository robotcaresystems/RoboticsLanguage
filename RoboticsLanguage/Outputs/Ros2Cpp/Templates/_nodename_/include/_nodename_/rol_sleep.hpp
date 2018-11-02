/*
 *  rol_timer.hpp
 *
 *  Created on: November 1, 2018
 *      Author: Dimitrios Chronopoulos
 *   Copyright: 2014-2018 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
 *
 */
#include <iostream>
#include <mutex>
#include <thread>
#include <chrono>
#include <atomic>

#ifndef ROL_UTILS_ROL_SLEEP_HPP
#define ROL_UTILS_ROL_SLEEP_HPP

using namespace std::chrono_literals;

namespace rol_sleep
{

  /**
  * @brief      Class used to block till a timeout with the option to unblock, i.e. an instance of this class
  *             can be used to set some thread to sleep and then some other thread can wake it up.
  *             The intended pattern of usage is: one thread sleeps another thread wakes the first up.
  *             If two or more threads try to sleep using the same sleeper, it is up to them to avoid ending up on a
  *             deadlock.
  *
  *             Code adapted from here:
  *             https://stackoverflow.com/questions/32233019/wake-up-a-stdthread-from-usleep
  */
  class Sleeper
  {
    public:

      // MEMBER METHODS

      /**
       * @brief   Constructor
       */
      Sleeper(){}

      /**
       * @brief   Destructor: Wakes up so any threads blocked by this sleeper will continue.
       */
      ~Sleeper(){
        unlock();
      }

      /**
       * @brief   Sleeps (blocks) for the given duration.
       *
       * @param   duration  A chrono literal specifying the sleep duration
       */
      template< typename DurationT >
      void sleep(const std::chrono::duration<int64_t, DurationT>& duration){
        // Lock the mutex (blocks if the mutex was already locked somehow).
        lock();
        // Try again to lock the mutex. This will block for the desired duration or untill the mutex is unlocked.
        /* @NOTE(d.chronopoulos):
         * It is not clear if there is a significant performance hit for using this method
         * instead of a normal sleep. It depends on the way the lock status is polled, i.e.
         * continously or with the thread 'yielding' in between. In any case if the overhead
         * proves to be high this can be replaced with a while-loop that measures the time passed and calls
         * try_lock and sleep on every cycle.
         *
         */
        mutex_.try_lock_for(duration);
        // Wake up
        unlock();
        return;
      }

      /**
       * @brief   Unlocks the mutex if needed.
       */
      void wake()
      {
        unlock();
        return;
      }

    private:

      // MEMBER METHODS

      /**
       * @brief   Locks mutex and raises flag.
       */
      void lock()
      {
        mutex_.lock();
        return;
      }

      /**
       * @brief   Unlocks mutex and lowers flag.
       */
      void unlock()
      {
        mutex_.unlock();
        return;
      }

      // MEMBER VARIABLES
      std::timed_mutex mutex_;    /**< A timed mutex that allows using try_lock_for */
  };

} // namespace rol_sleep

#endif // ROL_UTILS_ROL_SLEEP_HPP
