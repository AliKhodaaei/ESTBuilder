package P1;

class Test extends Sup
{
    int a = 9;
    {int c = 0;}
    public static int mtd(int b) throws java.util.ArithmeticException, ClassNotFoundException
    {
        int b = 0;
        a = b + 5;
        return 4;
    }


    void Caller()
    {
        int a = 78;
        int result = mtd(a);
    }
}
class Test2 implements ISup
{
    void Foram()
    {
        for (int i = 0; i < 5; i++)
        {
            a += i;
        }
    }
}