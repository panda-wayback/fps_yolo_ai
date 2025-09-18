from rx.subject import BehaviorSubject

value = BehaviorSubject(0)

def callback(new_value):
    print("Value changed to:", new_value)

value.subscribe(callback)

# 改变值
value.on_next(10)
value.on_next(20)
