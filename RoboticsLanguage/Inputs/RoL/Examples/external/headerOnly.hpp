




int addIntegers(int x, int y)
{
  return x+y;
}


int subtractIntegers(int x, int y)
{
  return x-y;
}

class LinearAlgebra
{
public:
  LinearAlgebra(double a, double b)
  {
    _a = a;
    _b = b;
  }
private:
  double _a;
  double _b;

  double inner3(double a1, double a2, double a3, double b1, double b2, double b3)
  {
    return a1*b1 + a2*b2 + a3*b3;
  }

};


LinearAlgebra test(1,2);

template <class T>
T addition(T a1, T a2)
{
  return a1 + a2;
}


namespace space
{


  double addDoubles(double x, double y)
  {
    return x+y;
  }

  double subtractDoubles(double x, double y)
  {
    return x+y;
  }


  class IntegerAlgebra
  {
    int inner3(int a1, int a2, int a3, int b1, int b2, int b3)
    {
      return a1*b1 + a2*b2 + a3*b3;
    }

  };

}





space::IntegerAlgebra test2;
