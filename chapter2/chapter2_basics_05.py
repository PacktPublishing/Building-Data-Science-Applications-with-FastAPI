def retrieve_page(page):
    if page > 3:
        return {"next_page": None, "items": []}
    return {"next_page": page + 1, "items": ["A", "B", "C"]}


items = []
page = 1
while page is not None:
    page_result = retrieve_page(page)
    items += page_result["items"]
    page = page_result["next_page"]


print(items)  # ["A", "B", "C", "A", "B", "C", "A", "B", "C"]
