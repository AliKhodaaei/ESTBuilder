class Simple
{
    int a = 1;
    void create()
    {
        a = 7;
    }

    void set()
    {
        create();
        {a = 44;}
    }
}