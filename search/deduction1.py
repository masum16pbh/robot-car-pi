def apply_modus_ponens(known_statements):
    inferred = set(known_statements)
    new_inferred = True

    while new_inferred:
        new_inferred = False
        for stmt in known_statements:
            if '->' in stmt:
                premise, conclusion = stmt.split('->')
                premise = premise.strip()
                conclusion = conclusion.strip()
                if premise in inferred and conclusion not in inferred:
                    inferred.add(conclusion)
                    new_inferred = True
    return inferred


def deduction_theorem(premises, conclusion):
    # premises = ['A', 'A -> B', 'B -> C']
    # conclusion = 'A -> C'

    if '->' not in conclusion:
        print("Conclusion must be in the form A -> B")
        return False

    A, B = conclusion.split('->')
    A = A.strip()
    B = B.strip()

    # Step 1: Add A to premises
    new_premises = premises + [A]

    # Step 2: Use Modus Ponens to derive B
    inferred = apply_modus_ponens(new_premises)

    if B in inferred:
        print(f"✅ By Deduction Theorem, {A} -> {B} is valid.")
        return True
    else:
        print(f"❌ Cannot derive {B} from premises + {A}")
        return False


# Example usage
premises = ['A', 'A -> B', 'B -> C']
conclusion = 'A -> C'

deduction_theorem(premises, conclusion)
