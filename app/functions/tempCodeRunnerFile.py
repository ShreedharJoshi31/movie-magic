A dictionary containing the success status and the Razorpay order object 
        if the creation was successful, or an error message if the operation failed.

        Example successful response:
        {
            "success": True,
            "order": {
                "id": "order_xxxxxxx",
                "entity": "order",
                "amount": 50000,
                "currency": "INR",
                "status": "created",
                ...
            }
        }

        Example failure response:
        {
            "success": False,
            "error": "Detailed error message"
        }

    Raises:
    ------
    ValueError:
        If the API credentials are not set in the environment variables.

    Example Usage:
    --------------
    response = create_razorpay_order(500)  # Create an order for 500 INR
    if response["success"]:
        print("Order created successfully:", response["order"])
    else:
        print("Order creation failed:", response["error"])
    """