import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

def create_razorpay_order(total_amount):
    """
    Creates a new order in Razorpay using the provided total amount.

    This function interacts with the Razorpay API to generate an order object 
    based on the specified total amount. The function fetches Razorpay API 
    credentials (`RAZORPAY_API_KEY` and `RAZORPAY_API_SECRET`) from environment 
    variables to authenticate the request. The amount is converted from INR to 
    paise as required by Razorpay.

    Parameters:
    ----------
    total_amount : float
        The total amount to be charged in Indian Rupees (INR).

    Returns:
    -------
    dict
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
    try:
        # Fetch Razorpay API keys from environment variables
        api_key = os.getenv("RAZORPAY_API_KEY")
        api_secret = os.getenv("RAZORPAY_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("Razorpay API credentials are not set in the environment variables.")

        # Initialize Razorpay client with the API key and secret
        client = razorpay.Client(auth=(api_key, api_secret))
        
        # Create order options
        options = {
            "amount": int(total_amount * 100),  # Convert amount to paise
            "currency": "INR",
        }
        
        # Create the order
        order = client.order.create(data=options)
        
        # Return success response with the order details
        return {"success": True, "order": order}
    
    except Exception as e:
        # Handle any errors that occur
        return {"success": False, "error": str(e)}
