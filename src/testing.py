def _sort_2_order(sort: str | None):
    if not sort:
        return "review_id", 1
    
    match sort[0]:
        case "+":
            return {"sort": f"{sort[1:]}:asc"}
        case "-":
            return {"sort": f"{sort[1:]}:desc"}
        case _:
            return {"sort": "id:asc"}
        
def some_function(ass, nigga):
    print(ass)
    print(nigga)


ass, nigga = _sort_2_order(sort=None)


