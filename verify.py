import casbin

e = casbin.Enforcer("model.conf", "0policy.csv")

sub = "alice"  # the user that wants to access a resource.
obj = "grade"  # the resource that is going to be accessed.
act = "add"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    # permit alice to read data1
    print("permit alice to read data1")
    pass
else:
    # deny the request, show an error
    print("deny the request, show an error")
    pass


