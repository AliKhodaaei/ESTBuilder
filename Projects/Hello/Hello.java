package jcg.zheng.demo.modifier;

import java.util;
import java.math;

// A simple Java program to demonstrate the use of variables, methods, and classes
public class MyDirty { // A class declaration
	public static int g = 9; // global variable
    public static void main(String[] args) { // A method declaration
        int x = 10; // A variable declaration and assignment
        final int y = 20; // Another variable declaration and assignment
        System.out.println("Hello, world!"); // A method invocation
        System.out.println("The sum of x and y is " + add(x, y)); // Another method invocation
    }
    class InnerDirty
    {
        int ij = 9;
    }

    public static int add(int a, int b) throws Exception, Exception2 { // Another method declaration
        return a + b; // A return statement
    }
}

public interface MyDirtyInterface
{
    class InnerInInterface {}
}

// An enum to represent different colors
enum Color {
    RED, GREEN, BLUE, YELLOW, BLACK, WHITE;
}

// A record to represent a point in 2D space
record Point(int x, int y) {
    // A constructor that validates the input
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordinates must be non-negative");
        }
    }
}