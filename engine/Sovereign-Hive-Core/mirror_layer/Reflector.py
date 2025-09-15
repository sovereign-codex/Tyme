# Reflector
# Observes the Hive and provides coherence reports

def reflect(hive_state):
    coherence = sum([1 for agent in hive_state if agent.get('active')]) / len(hive_state)
    return f"Hive Coherence: {coherence * 100:.2f}%"

# Placeholder state
if __name__ == '__main__':
    hive_state = [{'id': 1, 'active': True}, {'id': 2, 'active': False}]
    print(reflect(hive_state))