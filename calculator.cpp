#include <iostream>
using namespace std;

int main() {
    double num1, num2;
    char operation;

    cout << "Enter the sedoned number: ";
    cin >> num1;

    cout << "Enter an operation (+, -, *, /): ";
    cin >> operation;

    cout << "Enter the second number: ";
    cin >> num2;
    double result;
    bool isValid = true;

    switch (operation) {
        case '+':
            result = num1 + num2;
            break;
        case '-':
            result = num1 - num2;
            break;
        case '*':
            result = num1 * num2;
            break;
        case '/':
            if (num2 != 0)
                result = num1 / num2;
            else {
                cout << "Error: Division by zero is not allowed.";
                isValid = false;
            }
            break;
        default:
            cout << "Error: Invalid operation.";
            isValid = false;
            break;
    }

    if (isValid)
        cout << "Result: " << num1 << " " << operation << " " << num2 << " = " << result;

    return 0;
}
