

#include "library.hpp"

int multiplyIntegers(int x, int y)
{
  return x*y;
}

int divideIntegers(int x, int y)
{
  return x/y;
}


double Statistics::mean(double a1, double a2, double a3)
{
  return (a1 + a2 + a3) / 3;
}


namespace spaceLibrary
{


  double multiplyDoubles(double x, double y)
  {
    return x*y;
  }

  double divideDoubles(double x, double y)
  {
    return x/y;
  }


    bool Logic::andOperation(bool a, bool b)
    {
      return a && b;
    }

}
