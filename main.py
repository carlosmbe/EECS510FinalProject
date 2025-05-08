def read_automaton_from_string(data_str):
    lines = data_str.strip().split('\n')
    automaton = {
        'states': set(lines[0].split()),
        'alphabet': set(lines[1].split()),
        'start_state': lines[2].strip(),
        'accept_states': set(lines[3].split()),
        'transitions': {}
    }

    for line in lines[4:]:
        parts = line.strip().split()
        if len(parts) == 3:
            from_state, symbol, to_state = parts
            if from_state not in automaton['transitions']:
                automaton['transitions'][from_state] = {}
            if symbol not in automaton['transitions'][from_state]:
                automaton['transitions'][from_state][symbol] = []
            automaton['transitions'][from_state][symbol].append(to_state)

    return automaton

def accept(A, input_string):
    def helper_cleaner(s):
        note_chars = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'A', 'B', 'C', 'D', 'E', 'F', 'G'}
        return ''.join(['N' if char in note_chars else char for char in s])

    cleaned_string = helper_cleaner(input_string)
    symbols = list(cleaned_string)

    current_states = [(A['start_state'], [A['start_state']])]

    for symbol in symbols:
        next_states = []
        for state, path in current_states:
            if state in A['transitions'] and symbol in A['transitions'][state]:
                for next_state in A['transitions'][state][symbol]:
                    next_states.append((next_state, path + [next_state]))

        if not next_states:
            return 'reject'
        current_states = next_states

    for state, path in current_states:
        if state in A['accept_states']:
            return ('accept', path)

    return 'reject'

twelve_bar_NFA_automaton_data = """
q0 q1 q2 q3 q4 q5 q6 q7 q8 q9 q10 q11 N1 N2 N3 N4 N5 N6 N7 N8 N9 N10 N11 end
1 4 5 N
q0
end
q0 1 q1
q1 1 q2
q2 1 q3
q3 1 q4
q4 4 q5
q5 4 q6
q6 1 q7
q7 1 q8
q8 5 q9
q9 4 q10
q10 1 q11
q11 5 end
end 1 q1
q1 N N1
q2 N N2
q3 N N3
q4 N N4
q5 N N5
q6 N N6
q7 N N7
q8 N N8
q9 N N9
q10 N N10
q11 N N11
N1 N N1
N2 N N2
N3 N N3
N4 N N4
N5 N N5
N6 N N6
N7 N N7
N8 N N8
N9 N N9
N10 N N10
N11 N N11
N1 1 q2
N2 1 q3
N3 1 q4
N4 4 q5
N5 4 q6
N6 1 q7
N7 1 q8
N8 5 q9
N9 4 q10
N10 1 q11
N11 5 end
"""

A = read_automaton_from_string(twelve_bar_NFA_automaton_data)

print(accept(A, "111144115415")) # Most Basic 12 Bar Blues We Can Have
print(accept(A, "111N144N11N54N15")) # 12 Bar Blues With some melody

print(accept(A, "1abfd11GA1C44N1ab1N5N4N1N5")) # More complex 12 Bar Blues

print(accept(A, "a b c 1 4 5 A C D")) # Should fail
print(accept(A, "hello")) # Should fail