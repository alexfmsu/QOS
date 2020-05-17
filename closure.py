import copy

n = 3

state = [0] * n


# def cl(state):
#     s = state

#     def inc(state, i):
#         if state[i] == 0:
#             s = copy.copy(state)
#             s[i] = 1
#             return s

#     states = []

#     for i in range(len(s)):
#         states.append(inc(s, i))

#     return states


# def cl(state):
#     s = state

#     def inc(state, i):
#         # nonlocal s
#         if state[i] == 0:
#             s = state
#             # s = copy.copy(state)
#             s[i] = 1

#             if i == 2:
#                 s = state
#             print(state)
#             print(s)
#             exit(0)
#             return s

#     states = []

#     for i in range(len(s)):
#         states.append(inc(s, i))

#     return states

# print(state)

# state_cpy = copy.copy(state)

# i = 0
# state[i] = 2
# if i == 1:
#     state = state_cpy

# print(state)
# print(state_cpy)

# def cl(state, i):
#     state_ = copy.copy(state)

#     def ii(state):
#         def inc(st, i):
#             st[i] = 1

#             # if i == 1:
#             #     state = state_
#             #     return None
#             state = state_

#             return copy.copy(st)

#         # return inc(state_, i)

#         data = []

#         for j in range(3):
#             data.append(inc(state, j))
#             state = state_

#         return data

#     return ii(state)

data = []

state_cpy = copy.deepcopy(state)

for i in range(n):
    state_cpy[i] = 1

    if i == 1:
        to_add = None
        state_cpy = state
    else:
        to_add = state_cpy
        state_cpy = copy.deepcopy(state)

    data.append(to_add)

    # state_cpy = copy.deepcopy(state)

print(data)
# print(cl(state, 0))
# print(state)

# print(cl(state, 1))
# print(state)

# print(cl(state, 2))
