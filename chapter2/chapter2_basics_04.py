def forward_order_status(order):
    if order["status"] == "NEW":
        order["status"] = "IN_PROGRESS"
    elif order["status"] == "IN_PROGRESS":
        order["status"] = "SHIPPED"
    else:
        order["status"] = "DONE"
    return order


print(forward_order_status({"status": "NEW"}))  # {"status": "IN_PROGRESS"}
print(forward_order_status({"status": "IN_PROGRESS"}))  # {"status": "SHIPPED"}
print(forward_order_status({"status": "SHIPPED"}))  # {"status": "DONE"}
